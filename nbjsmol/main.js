define([
    "require",
    "jquery"
], function(
    require,
    $
) {
    "use_strict";

    //var jsmol_min_nojq = require('jsmol/JSmol.min.nojq');
    //var jsmol_min_nojq = require('jsmol/JSmol.min');
    function load_ipython_extension(){
        console.info('this is my first extension');
    }

    return {
	load_jupyter_extension : load_jupyter_extension,
	load_ipython_extension : load_jupyter_extension,
    };
});
