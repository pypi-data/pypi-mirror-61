// -*- coding: utf-8 -*-
// :Project:   metapensiero.extjs.desktop -- Custom standalone form label
// :Created:   lun 16 lug 2018 08:12:05 CEST
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2018 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/

Ext.define('MP.form.StandaloneLabel', {
    extend: 'Ext.form.Label',
    alias: 'widget.standalone-label',

    /**
     * Override the Label's behaviour that always inserts a “for”
     * attribute, eventually empty, even if its documentation says it
     * should not. This causes a “getElementById() called with an
     * empty string” warning in Firebug console.
     */
    getElConfig: function() {
        var me = this;

        me.html = me.text ? Ext.util.Format.htmlEncode(me.text) : (me.html || '');
        return Ext.form.Label.superclass.getElConfig.apply(me);
    }
});
