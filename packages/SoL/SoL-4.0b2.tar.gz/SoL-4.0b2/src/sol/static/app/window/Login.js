// -*- coding: utf-8 -*-
// :Project:   SoL -- Authentication form UI
// :Created:   lun 15 apr 2013 11:35:31 CEST
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2013, 2014, 2018, 2020 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/
/*jsl:declare __admin_email__ */
/*jsl:declare __password_reset__*/
/*jsl:declare __signin__*/

Ext.define('SoL.window.Login', {
    extend: 'MP.window.Login',
    width: 450,

    initComponent: function() {
        var me = this;

        me.callParent(arguments);

        var version = me.getDockedItems('toolbar[dock="bottom"] > label')[0];
        if(__admin_email__) {
            version.setText(
                Ext.String.format('<a href="{0}" target="_blank">{1}</a> &mdash; <a href="mailto:{2}?subject=SoL">{3}</a>',
                                  "https://gitlab.com/metapensiero/SoL/blob/master/CHANGES.rst",
                                  version.text,
                                  __admin_email__,
                                  '\uD83D\uDCE7 admin…'), false); // E-MAIL SYMBOL
        } else {
            version.setText(
                Ext.String.format('<a href="{0}" target="_blank">{1}</a> &mdash; <a href="{2}" target="_blank">{3}</a>',
                                  "https://gitlab.com/metapensiero/SoL/blob/master/CHANGES.rst",
                                  version.text,
                                  "/static/manual/index.html",
                                  _('About…')), false);
        }

        var tbitems = me.getDockedItems('toolbar[dock="bottom"]')[0];
        if(__signin__) {
            tbitems.insert(2, {
                xtype: 'button',
                text: _('Sign in…'),
                tooltip: _('Create a new account.'),
                action: 'signin',
                formBind: false
            });
        }
        if(__password_reset__) {
            tbitems.insert(2, {
                xtype: 'button',
                text: _('Lost password?'),
                tooltip: _('Request a reset of the password.'),
                action: 'lostpassword',
                formBind: false
            });
        }
    },

    getFormFields: function() {
        var me = this,
            fields = me.callParent();

        // Put a container with a logo and a description above the form fields

        fields.unshift({
            xtype: 'container',
            height: 100,
            html: [
                '<a href="/lit" data-qtip="',
                _('Go to the light HTML only interface…').replace(/"/g, '”'),
                '" target="_blank">',
                '  <img src="/static/images/logo.png"',
                '       style="margin-top: 15px; margin-left: 20px; float: left;">',
                '</a>',
                '<div style="margin-top: 25px; text-align: center;">',
                '<b>Scarry On Line</b><br/><br/>',
                _('Carrom tournaments management'),
                '</div>'
            ].join('')
        });

        return fields;
    }
});
