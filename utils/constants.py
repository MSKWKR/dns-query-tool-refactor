EMAIL_TABLE = {
    # domain
    "aspmx.l.google.com": "Google_Workspace",
    "smtp.google.com": "Gmail",
    "gmail-smtp-in.l.google.com": "Gmail",
    "outlook.com": "Office_365",
    "hinet.net": "HiNet_Mail",
    "amazon.com": "Amazon_SES",
    "yahoodns.net": "Yahoo!_Mail",
    "mailcloud.com": "Mailcloud",
    "Mimecast": "mimecast.com",
    "Messagelabs": "messagelabs.com",
    "ProofPoint": "pphosted.com",
    "中國移動": "chinamobile.com"
}

SRV_LIST = [
    '1password', 'a-d-sync', 'abi-instrument', 'accessdata-f2d', 'accessdata-f2w', 'accessone', 'accountedge',
    'acrobatsrv', 'actionitems', 'activeraid', 'activeraid-ssl', 'addressbook', 'adobe-vc', 'adisk',
    'adpro-setup', 'aecoretech', 'aeroflex', 'afpovertcp', 'airport', 'airprojector', 'airsharing',
    'airsharingpro', 'aix', 'amba-cam',
    'amiphd-p2p', 'animolmd', 'animobserver', 'anquetsync', 'appelezvous', 'apple-ausend', 'apple-midi',
    'apple-sasl', 'applerdbg',
    'appletv', 'appletv-itunes', 'appletv-pair', 'aquamon', 'asr', 'astnotify', 'astralite', 'async',
    'atlassianapp', 'autodiscover', 'av', 'axis-video', 'auth', 'b3d-convince', 'babyphone', 'bdsk', 'beacon',
    'beamer', 'beatpack', 'beep', 'bfagent', 'bigbangchess', 'bigbangmancala', 'bittorrent', 'blackbook',
    'bluevertise', 'bookworm', 'bootps', 'boundaryscan', 'bousg', 'bri', 'bsqdea', 'busycal', 'caldav',
    'caldavs', 'caltalk', 'cardsend', 'carddav', 'carddavs',
    'certificates', 'cctv', 'cheat', 'chess', 'chfts', 'chili', 'cip4discovery', 'clipboard', 'clique',
    'clscts', 'crl', 'crls', 'cmp', 'collection', 'com-ocs-es-mcc', 'contactserver', 'corroboree',
    'cpnotebook2', 'cvspserver', 'cw-codetap', 'cw-dpitap', 'cw-oncetap', 'cw-powertap', 'cytv', 'daap', 'dacp',
    'dancepartner', 'dataturbine', 'device-info', 'difi', 'disconnect', 'dist-opencl', 'distcc', 'ditrios',
    'divelogsync', 'dltimesync', 'dns-llq', 'dns-sd', 'dns-update', 'domain', 'dop', 'dossier', 'dpap',
    'dropcopy', 'dsl-sync', 'dtrmtdesktop', 'dvbservdsc', 'dxtgsync', 'ea-dttx-poker', 'earphoria', 'eb-amuzi',
    'ebms', 'ecms', 'ebreg', 'ecbyesfsgksc', 'edcp', 'egistix', 'eheap', 'embrace',
    'ep', 'eppc', 'erp-scale', 'esp', 'eucalyptus', 'eventserver', 'evs-notif', 'ewalletsync', 'example', 'exb',
    'exec', 'extensissn', 'eyetvsn', 'facespan', 'fairview', 'faxstfx', 'feed-sharing', 'firetask', 'finger',
    'fish', 'fix', 'fjork', 'fl-purr', 'fmpro-internal', 'fmserver-admin', 'fontagentnode', 'foxtrot-serv',
    'foxtrot-start', 'frameforge-lic', 'freehand', 'frog', 'ftp', 'ftpcroco', 'fv-cert', 'fv-key', 'fv-time',
    'garagepad', 'gbs-smp', 'gbs-stp', 'gc', 'gforce-ssmp', 'glasspad', 'glasspadserver', 'glrdrvmon', 'gpnp',
    'grillezvous', 'growl', 'guid', 'h323', 'h323be', 'h323cs', 'h323ls', 'helix', 'help', 'hg', 'hinz', 'hkp',
    'hkps', 'hmcp', 'home-sharing', 'homeauto', 'honeywell-vid', 'hotwayd', 'howdy', 'hpr-bldlnx', 'hpr-bldwin',
    'hpr-db', 'hpr-rep', 'hpr-toollnx', 'hpr-toolwin', 'hpr-tstlnx', 'hpr-tstwin', 'hs-off', 'htsp', 'http',
    'https', 'hydra', 'hyperstream', 'iax', 'ibiz', 'ica-networking', 'ican',
    'ichalkboard', 'ichat', 'iconquer', 'idata', 'idsync', 'ifolder', 'ihouse', 'ii-drills', 'ii-konane',
    'ilynx', 'imap', 'imaps', 'imidi', 'indigo-dvr', 'inova-ontrack', 'idcws', 'ipbroadcaster', 'ipp',
    'ipspeaker', 'irelay', 'irmc',
    'iscsi', 'isparx', 'ispq-vc', 'ishare', 'isticky', 'istorm', 'itis-device', 'itsrc', 'ivef', 'iwork',
    'jabber', 'jabber-client', 'jcan', 'jeditx', 'jini', 'jtag', 'kerberos', 'kerberos-adm', 'kpasswd', 'ktp',
    'labyrinth', 'lan2p',
    'lapse', 'lanrevagent', 'lanrevserver', 'ldap', 'leaf', 'lexicon', 'liaison', 'library', 'llrp',
    'llrp-secure', 'lobby', 'logicnode', 'login', 'lonbridge', 'lontalk', 'lonworks', 'lsys-appserver',
    'lsys-camera', 'lsys-ezcfg', 'lsys-oamp', 'lux-dtp', 'lxi', 'lyrics', 'macfoh', 'macfoh-admin',
    'macfoh-audio', 'macfoh-events', 'macfoh-data', 'macfoh-db', 'macfoh-remote', 'macminder', 'maestro',
    'magicdice', 'mandos', 'matrix', 'mbconsumer', 'mbproducer', 'mbserver', 'mconnect', 'mcrcp', 'mediaboard1',
    'mesamis', 'mimer', 'mi-raysat', 'modolansrv', 'moneysync', 'moneyworks', 'moodring', 'mother',
    'movieslate', 'mp3sushi', 'mqtt', 'mslingshot', 'mumble', 'musicmachine', 'mysync', 'mttp', 'mxim-art2',
    'mxim-ice', 'mxs', 'ncbroadcast', 'ncdirect', 'ncsyncserver', 'neoriders', 'net-assistant', 'net2display',
    'netrestore', 'newton-dock', 'nfs', 'nntp', 'nssocketport', 'ntlx-arch', 'ntlx-ent', 'ntlx-video', 'ntp',
    'ntx', 'obf', 'objective', 'oce', 'ocsp', 'od-master', 'odabsharing', 'odisk', 'officetime-sync',
    'ofocus-conf', 'ofocus-sync', 'olpc-activity1', 'oma-bcast-sg', 'omni-bookmark', 'omni-live', 'openbase',
    'opencu', 'oprofile', 'oscit', 'ovready', 'owhttpd', 'owserver', 'parentcontrol', 'passwordwallet', 'pcast',
    'p2pchat', 'panoply', 'parabay-p2p', 'parliant', 'pdl-datastream', 'pgpkey-hkp', 'pgpkey-http',
    'pgpkey-https', 'pgpkey-ldap', 'pgpkey-mailto', 'pgpkeys', 'pgprevokations', 'photoparata', 'pictua',
    'piesync', 'piu', 'pkixrep', 'poch', 'pokeeye', 'pop3', 'pop3s', 'postgresql', 'powereasy-erp',
    'powereasy-pos', 'pplayer-ctrl', 'presence', 'print-caps', 'printer', 'profilemac', 'prolog', 'protonet',
    'psap', 'psia', 'ptnetprosrv2', 'ptp', 'ptp-req', 'puzzle', 'qbox', 'qttp', 'quinn', 'rakket', 'radiotag',
    'radiovis', 'radioepg', 'raop', 'rbr', 'rce', 'rdp', 'realplayfavs', 'recipe', 'remote', 'remoteburn',
    'renderpipe', 'rendezvouspong', 'renkara-sync', 'resacommunity', 'resol-vbus', 'retrospect', 'rfb', 'rfbc',
    'rfid', 'riousbprint', 'roku-rcp', 'rql', 'rsmp-server', 'rsync', 'rtsp', 'rubygems', 'safarimenu',
    'sallingbridge', 'sallingclicker', 'salutafugijms', 'sandvox', 'sc-golf', 'scanner', 'schick', 'scone',
    'scpi-raw', 'scpi-telnet', 'sdsharing', 'see', 'seeCard', 'senteo-http', 'sentillion-vlc', 'sentillion-vlt',
    'sepvsync', 'serendipd', 'servereye', 'servermgr', 'services', 'sessionfs', 'sflow', 'sftp-ssh', 'shell',
    'shifter', 'shipsgm', 'shipsinvit', 'shoppersync', 'shoutcast', 'simmon', 'simusoftpong', 'sip',
    'sipfederationtls', 'sipinternal', 'sipinternaltls', 'sipuri', 'sips', 'sironaxray', 'skype', 'sleep-proxy',
    'slimcli', 'slimhttp', 'smartenergy', 'smb', 'sms', 'smtp', 'soap', 'socketcloud', 'sox', 'sparechange',
    'spearcat', 'spike', 'spincrisis', 'spl-itunes', 'spr-itunes', 'splashsync', 'ssh', 'ssscreenshare',
    'strateges', 'sge-exec', 'sge-qmaster', 'souschef', 'sparql', 'stanza', 'stickynotes', 'submission',
    'supple', 'surveillus', 'svcp', 'svn', 'swcards', 'switcher', 'swordfish', 'sxqdea', 'sybase-tds',
    'syncopation', 'syncqdea', 'synergy', 'synksharing', 'taccounting', 'tango', 'tapinoma-ecs',
    'taskcoachsync', 'tbricks', 'tcode', 'tcu', 'te-faxserver',
    'teamlist', 'teleport', 'telnet', 'tera-fsmgr', 'tera-mp', 'test', 'tf-redeye', 'tftp', 'thumbwrestling',
    'ticonnectmgr', 'timbuktu', 'tinavigator', 'tivo-hme', 'tivo-music', 'tivo-photos', 'tivo-remote',
    'tivo-videos', 'todogwa', 'tomboy', 'toothpicserver', 'touch-able', 'touch-remote', 'tri-vis-client',
    'tri-vis-server', 'tryst', 'tt4inarow',
    'ttcheckers', 'ttp4daemon', 'tunage', 'tuneranger', 'ubertragen', 'uddi', 'uddi-inq', 'uddi-pub',
    'uddi-sub', 'uddi-sec', 'upnp', 'urlbookmark', 'uswi', 'utest', 'uwsgi', 've-decoder', 've-encoder',
    've-recorder', 'visel', 'volley',
    'vos', 'vue4rendercow', 'vxi-11', 'walkietalkie', 'we-jell', 'webdav', 'webdavs', 'webissync', 'wedraw',
    'whamb', 'whois', 'whistler', 'wired', 'witap', 'witapvoice', 'wkgrpsvr', 'workstation', 'wormhole',
    'workgroup', 'writietalkie', 'ws', 'wtc-heleos', 'wtc-qels', 'wtc-rex', 'wtc-viscostar', 'wtc-wpr',
    'wwdcpic', 'x-on', 'x-plane9', 'x-puppet', 'x-puppet-ca', 'xcodedistcc', 'xgate-rmi', 'xgrid', 'xmms2',
    'xmp', 'xmpp-client', 'xmpp-server', 'xsanclient', 'xsanserver', 'xsansystem', 'xserveraid', 'xsync',
    'xtimelicence', 'xtshapro', 'xul-http', 'yakumo'
]

YELLOW_TITLE = "\033[1;33;40m"
BLANK_CUT = "\033[0m"
