feature_list = [ 
        "IP",
        "agent",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone", 

        "plugins", 
        "cookie", 
        "WebGL", 
        "localstorage", 
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest", 

        "inc", 
        "gpu", 
#        "gpuimgs", 
        "cpucores", 
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",

        "ipcity",
        "ipregion",
        "ipcountry",

        "fp2_liedlanguages",
        "fp2_liedresolution",
        "fp2_liedos",
        "fp2_liedbrowser",

        "browserfingerprint"
        ]

qfingerprint_change_feature_list = [
        "userAgentHttp",
        #"httpheaders",
        #"accept",
        "encodingHttp",
        "languageHttp",
        "timezoneJS",

        "pluginsJS",
        "localJS",
        "adBlock",
        "osDetailed",
        "fontsFlash",
        "canvasJS",

        "resolutionJS",

        ]
ori_feature_list = [ 
        "IP",
        "agent",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone", 

        "plugins", 
        "cookie", 
        "WebGL", 
        "localstorage", 
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest", 

        "inc", 
        "gpu", 
        "gpuimgs", 
        "cpucores", 
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",

        "fp2_liedlanguages",
        "fp2_liedresolution",
        "fp2_liedos",
        "fp2_liedbrowser",

        "clientid",
        "label",
        "uniquelabel",
        "time",
        "browserfingerprint"
        ]

fingerprint_feature_list = [
        "agent",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone", 

        "plugins", 
        "cookie", 
        "WebGL", 
        "localstorage", 
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest", 

        "inc", 
        "gpu", 
        "cpucores", 
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",
        "resolution",

        "ipcity",
        "ipregion",
        "ipcountry",

        "fp2_liedlanguages",
        "fp2_liedresolution",
        "fp2_liedos",
        "fp2_liedbrowser"
        ]

table_feature_list = [
        "agent",
        "browser",
        "os",
        "device",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone", 

        "plugins", 
        "cookie", 
        "WebGL", 
        "localstorage", 
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest", 

        "inc", 
        "gpu", 
        "partgpu",
        "gpuimgs", 
        "cpucores", 
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",
        "resolution",

        "ipcity",
        "ipregion",
        "ipcountry",

        "fp2_liedlanguages",
        "fp2_liedresolution",
        "fp2_liedos",
        "fp2_liedbrowser",
        "browserfingerprint",
        "noipfingerprint"
        ]

fingerprint_change_feature_list = [
        "agent",
        "os",
        "osversion",
        "browser",
        "browserversion",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone", 

        "langsdetected",
        #"label",
        "plugins", 
        "cookie", 
        "WebGL", 
        "localstorage", 
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest", 

        "inc", 
        "gpu", 
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",
        "cpucores",

        "ipcity",
        "ipregion",
        "ipcountry"

        #"fp2_liedlanguages",
        #"fp2_liedresolution",
        #"fp2_liedos",
        #"fp2_liedbrowser"
        ]

fingerprint_change_feature_list_temp = [
        # "agent",
        "os",
        "osversion",
        "browserversion",
        "engineversion",
        "doNotTrack",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone",

        "plugins",
        "cookie",
        "WebGL",
        "localstorage",
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest",

        "inc",
        "gpu",
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",

        #"ipcity",
        #"ipregion",
        #"ipcountry",

        "fp2_liedlanguages",
        "fp2_liedresolution",
        "fp2_liedos",
        "fp2_liedbrowser"
        ]

fingerprint_feature_list_include_gpuimgs = [
        "agent",
        "httpheaders",
        "accept",
        "encoding",
        "language",
        "timezone", 

        "plugins", 
        "cookie", 
        "WebGL", 
        "localstorage", 
        "fp2_addbehavior",
        "fp2_opendatabase",

        "langsdetected",
        "jsFonts",
        "canvastest", 

        "inc", 
        "gpu", 
        "gpuimgs", 
        "cpucores", 
        "audio",
        "fp2_cpuclass",
        "fp2_colordepth",
        "fp2_pixelratio",
        "resolution",

        "ipcity",
        "ipregion",
        "ipcountry",

        "fp2_liedlanguages",
        "fp2_liedresolution",
        "fp2_liedos",
        "fp2_liedbrowser",
        ]

browserid_list = [
        'clientid',
        'browser',
        'os',
        'device',
        'cpucores',
        'fp2_cpuclass',

        # SPECIAL FEATURE                   
        'WebGL',

        'partgpu'
        ]


def get_ori_feature_list():
    return ori_feature_list

def get_feature_list():
    return feature_list

def get_fingerprint_feature_list():
    return fingerprint_feature_list

def get_fingerprint_change_feature_list():
    return fingerprint_change_feature_list

def get_table_feature_list():
    return table_feature_list

def get_fingerprint_feature_list_include_gpuimgs():
    return fingerprint_feature_list_include_gpuimgs

def get_browserid_list():
    return browserid_list

def mobile_or_not(agent):
    mobile_str = 'Mobile|iPhone|iPod|iPad|Android|BlackBerry|IEMobile|Kindle|NetFront|Silk-Accelerated|hpwOS|webOS|Fennec|Minimo|Opera Mobi|Mini|Blazer|Dolfin|Dolphin|Skyfire|Zune'
    test_str = mobile_str.split('|')
    for test in test_str:
        if agent.find(test) != -1:
            return 1
    return 0

