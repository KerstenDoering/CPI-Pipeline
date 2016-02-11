import sys
import os
import locale
locale.setlocale(locale.LC_ALL, '')

# adjust basepath to the location of this file (jsreconfig.py)
basepath = '/vol/home-vol3/wbi/thomas/workspace/ppi-benchmark/Kernels/jsre/experiments'

jsre = basepath + "/../source/"
jsre_classpath = jsre + '/bin:' + jsre + '/lib/*'
#does not work due to missing  distance: 
#jsre_classpath = jsre + '/dist/xjsre.jar:' + jsre + '/lib/*' 

# nothing to set below

if not os.path.exists(basepath) or os.path.isfile(basepath):
        print >> sys.stderr, 'FATAL: Error accessing base directory ' + basepath + '!'
        sys.exit(1)

if not os.path.exists(jsre) or os.path.isfile(jsre):
        print >> sys.stderr, 'FATAL: Error accessing jsre directory ' + jsre + '!'
        sys.exit(1)

sys.path.append(basepath + '/measures')



