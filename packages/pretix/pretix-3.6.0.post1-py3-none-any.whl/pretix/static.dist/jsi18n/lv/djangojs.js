

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n % 10 == 0 || n % 100 >= 11 && n % 100 <= 19) ? 0 : ((n % 10 == 1 && n % 100 != 11) ? 1 : 2);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "(one more date)": [
      "(neviens datums)",
      "(v\u0113l viens datums)",
      "(v\u0113l {num} datumi)"
    ],
    "All": "Visi",
    "An error has occurred.": "Ir radusies k\u013c\u016bda.",
    "An error of type {code} occurred.": "Ir notikusi k\u013c\u016bda {code}.",
    "April": "Apr\u012blis",
    "August": "Augusts",
    "Barcode area": "Sv\u012btru koda lauks",
    "Calculating default price\u2026": "Apr\u0113\u0137ina pamata cenu\u2026",
    "Cart expired": "Pirkumu groza rezerv\u0101cijas laiks ir beidzies",
    "Check-in QR": "Re\u0123istr\u0101cijas QR",
    "Click to close": "Noklik\u0161\u0137iniet, lai aizv\u0113rtu",
    "Close message": "Aizv\u0113rt zi\u0146u",
    "Comment:": "Koment\u0101ri:",
    "Confirming your payment \u2026": "J\u016bsu maks\u0101jums tiek apstr\u0101d\u0101ts \u2026",
    "Contacting Stripe \u2026": "Savienojas ar Stripe \u2026",
    "Contacting your bank \u2026": "Tiek veidots savienojums ar j\u016bsu banku \u2026",
    "Copied!": "Nokop\u0113ts!",
    "Count": "Skaits",
    "December": "Decembris",
    "Do you really want to leave the editor without saving your changes?": "Vai j\u016bs tie\u0161\u0101m v\u0113laties iziet no redi\u0123\u0113\u0161anas lauka bez veikto izmai\u0146u saglab\u0101\u0161anas?",
    "Error while uploading your PDF file, please try again.": "Radusies k\u013c\u016bda aug\u0161upiel\u0101d\u0113jot j\u016bsu PDF failu, l\u016bdzu, m\u0113\u0123iniet v\u0113lreiz.",
    "February": "Febru\u0101ris",
    "Fr": "Pi",
    "Generating messages \u2026": "Zi\u0146as tiek \u0123ener\u0113tas \u2026",
    "Group of objects": "Objektu grupa",
    "January": "Janv\u0101ris",
    "July": "J\u016blijs",
    "June": "J\u016bnijs",
    "Lead Scan QR": "Galven\u0101s sken\u0113\u0161anas QR",
    "March": "Marts",
    "Marked as paid": "Atz\u012bm\u0113ts k\u0101 apmaks\u0101ts",
    "May": "Maijs",
    "Mo": "Pi",
    "No": "N\u0113",
    "None": "Neviens",
    "November": "Novembris",
    "Object": "Objekts",
    "October": "Oktobris",
    "Others": "Citi",
    "Paid orders": "Apmaks\u0101tie pas\u016bt\u012bjumi",
    "Placed orders": "Pieteiktie pas\u016bt\u012bjumi",
    "Please enter a quantity for one of the ticket types.": "L\u016bdzu, ievadiet nepiecie\u0161amo daudzumu izv\u0113l\u0113tajam bi\u013ce\u0161u veidam.",
    "Powered by pretix": "Pretix atbalst\u012bts",
    "Press Ctrl-C to copy!": "Nospiediet Ctrl-C, lai nokop\u0113tu!",
    "Sa": "Se",
    "Saving failed.": "Saglab\u0101\u0161ana neizdev\u0101s.",
    "September": "Septembris",
    "Su": "Sv",
    "Text object": "Teksta objekts",
    "Th": "Ce",
    "The PDF background file could not be loaded for the following reason:": "Fona PDF fails nevar\u0113ja iel\u0101d\u0113ties sekojo\u0161a iemesla d\u0113\u013c:",
    "The items in your cart are no longer reserved for you.": "J\u016bsu groz\u0101 saglab\u0101taj\u0101m prec\u0113m rezerv\u0101cijas laiks ir beidzies.",
    "The items in your cart are reserved for you for one minute.": [
      "Preces j\u016bsu groz\u0101 ir rezerv\u0113tas nulle min\u016btes.",
      "Preces j\u016bsu groz\u0101 ir rezerv\u0113tas uz vienu min\u016bti.",
      "Preces j\u016bsu groz\u0101 ir rezerv\u0113tas uz {num} min\u016bt\u0113m."
    ],
    "Ticket design": "Bi\u013ce\u0161u dizains",
    "Total": "Kop\u0101",
    "Total revenue": "Apgroz\u012bjums kop\u0101",
    "Tu": "Ot",
    "Unknown error.": "Nezin\u0101ma k\u013c\u016bda.",
    "Use a different name internally": "Izmantojiet citu nosaukumu iek\u0161\u0113ji",
    "We": "Tr",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "J\u016bsu piepras\u012bjums \u0161obr\u012bd tiek s\u016bt\u012bts uz serveri apstr\u0101dei. Ja \u0161is process aiz\u0146em ilg\u0101k k\u0101 vienu min\u016bti, l\u016bdzu, p\u0101rbaudiet savu interneta savienojumu, p\u0101rl\u0101d\u0113jiet \u0161o lapu un m\u0113\u0123iniet v\u0113lreiz.",
    "We are processing your request \u2026": "M\u0113s apstr\u0101d\u0101jam j\u016bsu piepras\u012bjumu \u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "M\u0113s patreiz nevaram izveidot savienojumu ar serveri, bet turpin\u0101m m\u0113\u0123in\u0101t. P\u0113d\u0113j\u0101s k\u013c\u016bdas kods: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "\u0160obr\u012bd neizdodas izveidot savienojumu ar serveri. L\u016bdzu m\u0113\u0123iniet v\u0113lreiz. K\u013c\u016bdas kods: {code}",
    "Yes": "J\u0101",
    "Your color has bad contrast for text on white background, please choose a darker shade.": "Izv\u0113l\u0113t\u0101 kr\u0101sa tekstam neizce\u013cas uz eso\u0161\u0101 fona, l\u016bdzu, izv\u0113lieties tum\u0161\u0101ku kr\u0101su.",
    "Your color has decent contrast and is probably good-enough to read!": "Izv\u0113l\u0113t\u0101 teksta kr\u0101sa pietiekami izce\u013cas un visdr\u012bz\u0101k b\u016bs sam\u0113r\u0101 viegli las\u0101ma!",
    "Your color has great contrast and is very easy to read!": "Izv\u0113l\u0113t\u0101 teksta kr\u0101sa \u013coti labi izce\u013cas un ir viegli las\u0101ma!",
    "Your request arrived on the server but we still wait for it to be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "J\u016bsu piepras\u012bjums v\u0113l st\u0101v rind\u0101 server\u012b uz apstr\u0101di. Ja gaid\u012b\u0161anas process aiz\u0146em ilg\u0101k k\u0101 divas min\u016btes, l\u016bdzu, sazinieties ar mums vai p\u0101rl\u0101d\u0113jiet savu interneta p\u0101rluku un m\u0113\u0123iniet v\u0113lreiz.",
    "Your request has been queued on the server and will now be processed. Depending on the size of your event, this might take up to a few minutes.": "J\u016bsu piepras\u012bjums ir ievietots rind\u0101 server\u012b un dr\u012bz tiks apstr\u0101d\u0101ts. Atkar\u012bb\u0101 no piepras\u012bjuma izm\u0113ra, process var aiz\u0146emt l\u012bdz da\u017e\u0101m min\u016bt\u0113m.",
    "widget\u0004Back": "Atpaka\u013c",
    "widget\u0004Buy": "Pirkt",
    "widget\u0004Choose a different date": "Izv\u0113l\u0113ties citu datumu",
    "widget\u0004Choose a different event": "Izv\u0113l\u0113ties citu pas\u0101kumu",
    "widget\u0004Close": "Aizv\u0113rt",
    "widget\u0004Close ticket shop": "Aizv\u0113rt bi\u013ce\u0161u veikalu",
    "widget\u0004Continue": "Turpin\u0101t",
    "widget\u0004FREE": "Bezmaksas",
    "widget\u0004Next month": "N\u0101kamais m\u0113nesis",
    "widget\u0004Only available with a voucher": "Pieejams tikai ar kuponu",
    "widget\u0004Open seat selection": "Atv\u0113rt s\u0113dvietu izv\u0113lni",
    "widget\u0004Previous month": "Iepriek\u0161\u0113jais m\u0113nesis",
    "widget\u0004Redeem": "Izmantot",
    "widget\u0004Redeem a voucher": "Izmantot kuponu",
    "widget\u0004Register": "Re\u0123istr\u0113ties",
    "widget\u0004Reserved": "Rezerv\u0113ts",
    "widget\u0004Resume checkout": "Turpin\u0101t veikt pirkumu",
    "widget\u0004See variations": "Apskat\u012bt iesp\u0113jas",
    "widget\u0004Sold out": "Izp\u0101rdots",
    "widget\u0004The cart could not be created. Please try again later": "Iepirkumu grozu nebija iesp\u0113jams izveidot. L\u016bdzu m\u0113\u0123iniet v\u0113lreiz v\u0113l\u0101k",
    "widget\u0004The ticket shop could not be loaded.": "Bi\u013ce\u0161u veikals nevar\u0113ja iel\u0101d\u0113ties.",
    "widget\u0004Voucher code": "Kupona kods",
    "widget\u0004Waiting list": "Gaid\u012b\u0161anas saraksts",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "Jums \u0161obr\u012bd jau ir akt\u012bvs pirkumu grozs \u0161im pas\u0101kumam. Ja atlas\u012bsiet papildus produktus, tie tiks pievienoti eso\u0161ajam grozam.",
    "widget\u0004currently available: %s": "\u0161obr\u012bd pieejams: %s",
    "widget\u0004from %(currency)s %(price)s": "no %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "iek\u013c. %(rate)s% %(taxname)s",
    "widget\u0004incl. taxes": "iek\u013c. nodok\u013cus",
    "widget\u0004minimum amount to order: %s": "minim\u0101lais pirkuma apjoms: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "plus %(rate)s% %(taxname)s",
    "widget\u0004plus taxes": "plus nodok\u013ci"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "Y. \\g\\a\\d\\a j. F, H:i",
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%d.%m.%Y %H:%M:%S",
      "%d.%m.%Y %H:%M:%S.%f",
      "%d.%m.%Y %H:%M",
      "%d.%m.%Y",
      "%d.%m.%y %H:%M:%S",
      "%d.%m.%y %H:%M:%S.%f",
      "%d.%m.%y %H:%M",
      "%d.%m.%y %H.%M.%S",
      "%d.%m.%y %H.%M.%S.%f",
      "%d.%m.%y %H.%M",
      "%d.%m.%y",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "Y. \\g\\a\\d\\a j. F",
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d",
      "%d.%m.%Y",
      "%d.%m.%y"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j. F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "j.m.Y H:i",
    "SHORT_DATE_FORMAT": "j.m.Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M",
      "%H.%M.%S",
      "%H.%M.%S.%f",
      "%H.%M"
    ],
    "YEAR_MONTH_FORMAT": "Y. \\g. F"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

