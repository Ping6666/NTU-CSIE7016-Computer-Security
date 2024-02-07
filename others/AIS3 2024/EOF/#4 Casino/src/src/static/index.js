// returns the cookie with the given name,
// or undefined if not found
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}


async function sha512(message) {
    return (new Hashes.SHA512).hex(message);
}


function animationDuration(totalDuration, offset, numOfTimes) {
    const easeOutCorrection = offset;
    const unit = numOfTimes * 10 + offset + easeOutCorrection;
    return totalDuration / unit * 10;
}

function transitionDuration(totalDuration, offset, numOfTimes) {
    const easeOutCorrection = offset;
    const unit = numOfTimes * 10 + offset + easeOutCorrection;
    return totalDuration / unit * (offset + easeOutCorrection);
}


function fetchGet(url, data) {
    const queryString = Object.entries(data).map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join('&');
    return fetch(url + '?' + queryString).then(resp => {
        if (!resp.ok) {
            throw resp.json();
        }
        return resp;
    });
}


function fetchPost(url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(resp => {
        if (!resp.ok) {
            throw resp.json();
        }
        return resp;
    });
}

function fetchPut(url, data) {
    return fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(resp => {
        if (!resp.ok) {
            throw resp.json();
        }
        return resp;
    });
}


document.addEventListener('alpine:init', () => {

    Alpine.data('app', () => ({
        teamToken: '', // this is the token for the contest
        userCredential: null, // this is the credential of this casino challenge
        luckyNumber: [0, 0, 0],
        roundID: null,
        balance: 0,
        bet: 100,
        prizePool: 0,
        get machineID() {
            const hostname = window.location.hostname;
            const machineID = parseInt(hostname.split('.')[1]);
            return (1 <= machineID && machineID <= 10) ? machineID : 1;
        },

        notificationClass: '',
        notificationContent: '',

        animationManager: new AnimationManager(),
        roundManager: null,

        init() {
            this.roundManager = new RoundManager(this);

            // check if cookie has user credential
            const teamToken = getCookie('teamToken');
            if (teamToken) {
                this.teamToken = decodeURIComponent(teamToken);
                this.initApp();
            }
        },

        async initApp() {
            const success = await this.roundManager.start();
            if (!success) {
                this.notificationClass = 'is-warning';
                this.notificationContent = 'Invalid team token.';
                return;
            }
            this.notificationContent = '';

            // set cookie
            document.cookie = `teamToken=${encodeURIComponent(this.teamToken)}; path=/; max-age=172800`;
        },

        logout() {
            // clear cookie
            this.teamToken = null;
            this.userCredential = null;
            this.roundManager.stop();
            document.cookie = `teamToken=; path=/; max-age=-1`;
        },

        async fetchPrizePool() {
            const resp = await fetchGet(`${URL_GET_POOL}/${this.machineID}`, {});
            const {value} = await resp.json();
            this.prizePool = value;
        },

        async spinSlotMachine() {
            // prevent re-entrance
            if (this._isSpinning === undefined) {
                this._isSpinning = false;
            }
            if (this._isSpinning) {
                return;
            }
            this._isSpinning = true;
            this.roundManager.stopFetchBalanceTemporarily = true;

            try {
                // 1st step: get challenge number from backend
                const resp = await fetchPost(URL_START_GAME, {
                    user_token: await sha512(this.userCredential),
                    bet: this.bet,
                });
                const gameID = (await resp.json()).game_id;

                // 2nd step: get the random result
                const resp2 = await fetchPut(URL_RESULT, {
                    user_token: this.userCredential,
                    game_id: gameID,
                    bet: this.bet,
                });
                const {random_number: randomNumber, result: result} = await resp2.json();
                const randomDigits = [Math.floor(randomNumber / 100), Math.floor((randomNumber % 100) / 10), randomNumber % 10];
                console.debug('randomDigits', randomDigits);

                // 3rd step: animate the slot machine
                await this.animationManager.run(randomDigits);

                // 4th step: update balance
                this.roundManager.stopFetchBalanceTemporarily = false;
                await this.roundManager.fetchBalance();

                // 5th step: show notification if result is not 0
                if (result > 0) {
                    this.notificationClass = 'is-info';
                    this.notificationContent = `Congratulations! You won ${result} points!`;
                }

            } catch (e) {
                // if e is promise, await it
                if (e instanceof Promise) {
                    e = await e;
                }
                console.error(e);
                this.notificationClass = 'is-danger';
                this.notificationContent = `An error occurred. ${JSON.stringify(e)}`;

            } finally {
                this._isSpinning = false;
                this.roundManager.stopFetchBalanceTemporarily = false;
            }
        },
    }));
});


class AnimationManager {
    constructor() {
        this.spinArmAnimation = null;
        this.rainbowBoxAnimation = null;
        this.slotDigitElement = [null, null, null];
        this.slotDigitClassPrefix = '';
        this.slotDigit = [0, 0, 0];
        this.audio = null;
    }

    addSpinArmAnimation(element, transitionName) {
        this.spinArmAnimation = {element, transitionName};
    }

    addSlotDigitAnimation(element, slotDigitClassPrefix, index) {
        this.slotDigitElement[index] = element;
        this.slotDigitClassPrefix = slotDigitClassPrefix;
    }

    addRainbowBoxAnimation(element, animationName) {
        this.rainbowBoxAnimation = {element, animationName};
    }

    addAudio(audioPath) {
        this.audio = new Audio(audioPath);
    }

    async run(randomDigits) {
        // play audio from start
        this.audio.pause();
        this.audio.currentTime = 0;
        this.audio.play();

        // start rainbow box animation
        this.rainbowBoxAnimation.element.classList.add(this.rainbowBoxAnimation.animationName);

        // start other animations
        const spinArmAnimationPromise = this._transitionOnce(this.spinArmAnimation.element, this.spinArmAnimation.transitionName);
        const slotDigitAnimationPromise = [0, 1, 2].map(i => this._animationSlotDigitOnce(this.slotDigitElement[i], i, randomDigits[i]));
        await Promise.all([
            spinArmAnimationPromise,
            ...slotDigitAnimationPromise,
        ]);

        // stop rainbow box animation
        this.rainbowBoxAnimation.element.classList.remove(this.rainbowBoxAnimation.animationName);
    }

    async _transitionOnce(element, transitionName) {
        // To prevent race condition, the promise must be created before the transition starts.
        const transitionEndPromisePre = new Promise(resolve => element.addEventListener('transitionend', resolve, {once: true}));
        element.classList.add(transitionName);
        await transitionEndPromisePre;

        const transitionEndPromisePost = new Promise(resolve => element.addEventListener('transitionend', resolve, {once: true}));
        element.classList.remove(transitionName);
        await transitionEndPromisePost;
        // TODO: remove event listener
    }

    async _animationOnce(element, animationName) {
        const animationEndPromise = new Promise(resolve => element.addEventListener('animationend', resolve, {once: true}));
        element.classList.add(animationName);
        await animationEndPromise;

        element.classList.remove(animationName);
        // TODO: remove event listener
    }

    async _animationSlotDigitOnce(element, index, digit) {
        const slotDigitClassOld = `${this.slotDigitClassPrefix}-${index}-${this.slotDigit[index]}`;
        const slotDigitClassNew = `${this.slotDigitClassPrefix}-${index}-${digit}`;

        // clean up the previous digit (may cause transition but we don't care)
        element.classList.remove(slotDigitClassOld + '-transition');

        // spin the digit
        await this._animationOnce(element, slotDigitClassNew + '-animation');

        // finalizing the digit
        await new Promise(resolve => setTimeout(resolve, 0)); // wait for the transition to start
        const transitionEndPromise = new Promise(resolve => element.addEventListener('transitionend', resolve, {once: true}));
        element.classList.add(slotDigitClassNew + '-transition');
        await transitionEndPromise;
        this.slotDigit[index] = digit;
        // TODO: remove event listener
    }
}


class RoundManager {
    constructor(app) {
        this.app = app;
        this.intervalID = null;
        this.fetchPrizePoolIntervalID = null;

        this.stopFetchBalanceTemporarily = false; // if the slot machine is spinning, we don't want to update the balance
    }

    async start() {
        const success = await this.fetchRoundInfo();
        if (!success) {
            return false;
        }
        await this.fetchBalance();
        await this.app.fetchPrizePool();

        this.intervalID = setInterval(() => {
            this.fetchRoundInfo();
            this.fetchBalance();
        }, 3000);
        this.fetchPrizePoolIntervalID = setInterval(() => {
            this.app.fetchPrizePool();
        }, 1000);
        return true;
    }

    stop() {
        clearInterval(this.intervalID);
        clearInterval(this.fetchPrizePoolIntervalID);
    }

    async fetchRoundInfo() {
        // get round info from backend using team token
        const resp = await fetchGet(URL_ROUND_INFO, {
            team_token: this.app.teamToken,
        });
        if (!resp.ok) {
            return false;
        }
        const {user_token: userToken, lucky_number: luckyNumber, round_id: roundID} = await resp.json();
        this.app.userCredential = userToken;
        this.app.luckyNumber = [Math.floor(luckyNumber / 100), Math.floor((luckyNumber % 100) / 10), luckyNumber % 10];
        this.app.roundID = roundID;

        return true;
    }

    async fetchBalance() {
        if (this.stopFetchBalanceTemporarily) {
            return;
        }

        // get balance
        const resp = await fetchGet(URL_GET_BALANCE, {
            user_token: this.app.userCredential,
        });
        const {balance} = await resp.json();
        this.app.balance = balance;
    }
}
