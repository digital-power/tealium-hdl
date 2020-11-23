// Set hdl_lookup variable from a specific JS value or meta/html data
var hdl_lookup = 'datalayer-page-1'

// Define account variables
var account =  ''
var profile = ''

// Get HDL datalayer data if available
var path = "https://tags.tiqcdn.com/dle/" + account + "/" + profile + "/";
// Reset any data previous HDL values
utag.globals = {dle:{enrichments:{}}};
    // Get data from HDL
    utag.ut.loader({
    src: path + hdl_lookup + ".js",
    cb: function(){
    utag_data.hdl_enrichment = utag.globals.dle.enrichments[hdl_lookup];
        // check if hdl_enrichment is filled by HDL dataLayer request
        if(typeof utag_data.hdl_enrichment != "undefined") {
            //merge variables from hdl_enrichment with utag_data
            utag.ut.merge(utag_data,utag_data.hdl_enrichment,1);
        } else {
            //Do something else, like making default values filled or missing mapping info
        };
    }
});
