DESCRIPTION = \
'''
#--------------------------------------------------------------------------------------------------
  Convert Microsoft Word and Excel files from one file format to another.
#--------------------------------------------------------------------------------------------------
'''

EPILOG = \
'''
#--------------------------------------------------------------------------------------------------

This script automates the Microsoft Word and Excel applications to open a Word or Excel file in one 
format, and save it in another.

A common use case might be to convert Word documents in the older 97-2003 binary '.doc' format
to the newer Open XML '.docx' file format.

The script required >= python 3.5  

The script recursively scans from a base directory and writes out each file in the new format, 
to the same directory as the original source file.

e.g. C:\\foo\\a\\word_document_1.doc     <-- Original
     C:\\foo\\a\\word_document_1.docx    <-- New
     C:\\foo\\a\\b\word_document_2.doc   <-- Original
     C:\\foo\\a\\b\\word_document_2.docx  <-- New

## Study the formats in the links below to understand which output formats can be selected. 

https://docs.microsoft.com/en-us/office/vba/api/word.wdsaveformat
https://docs.microsoft.com/en-us/office/vba/api/excel.xlfileformat

## Example script use

# Convert from Word '.doc' to '.docx' format, scan starting from the user HOME directory.
# Converting from '.doc' to '.docx', starting from the HOME directory is the script default setting.

    python.exe microsoft_doc_converter.py

# Same as above, except as a Dryrun. In Dryrun mode the files to be converted are just listed,
# not converted.

    python.exe microsoft_doc_converter.py --dryrun

# Convert from Word '.doc' to '.docx' format, scan starting from the C:\\foo directory.

    python.exe microsoft_doc_converter.py --basedir "C:\\foo" 

# Convert from Word '.docx' to '.pdf' format, scan starting from the C:\\foo directory.

    python.exe microsoft_doc_converter.py -b "C:\\foo" -s "docx" -d "pdf" -f 17

# Convert from Excel '.xls' to '.xlsx' format, scan starting from the C:\\bar directory.

    python.exe microsoft_doc_converter.py -c "Excel.application" -b "C:\\bar" -s "xls" -d "xlsx" -f 51

#--------------------------------------------------------------------------------------------------

## !! BIG FAT WARNING !! 

File conversions can result in changed/lost content and formatting.
As always, backups and lots of testing is advised.

#--------------------------------------------------------------------------------------------------

# Briefly tested, May 3rd 2020, using,
    - Anaconda3-2020.02-Windows-x86_64.exe (Python 3.7.6)
    - Windows 10 Enterprise 1909
    - Microsoft Office 365 ProPlus, Version 1908

#--------------------------------------------------------------------------------------------------
'''
#--------------------------------------------------------------------------------------------------

__author__ = 'Dave Coutts'
__license__ = 'Apache'
__version__ = '1.0.0'
__maintainer__ = 'https://github.com/davecoutts'
__status__ = 'Production'

#--------------------------------------------------------------------------------------------------

import win32com.client
from pathlib import Path

#--------------------------------------------------------------------------------------------------

def converter(comObject, dirPath, sourceExtension, destinationExtension, fileFormat, dryRun=False):
    
    msApp = win32com.client.Dispatch(comObject)
    
    for sourceFile in sorted(dirPath.rglob(f'*.{sourceExtension}')):
        
        destinationFile = sourceFile.with_suffix(f'.{destinationExtension}')
        
        if not destinationFile.is_file():
        
            print(f'Converting: {sourceFile}')
        
            if not dryRun:
        
                try:

                    if comObject == 'Excel.application':
        
                        doc = msApp.Workbooks.Open(str(sourceFile))
        
                    elif comObject == 'Word.application':
        
                        doc = msApp.Documents.Open(str(sourceFile))
        
                    doc.SaveAs(str(destinationFile), FileFormat = fileFormat)
        
                    doc.Close()
        
                except Exception as e:
        
                    print(f'Failed to Convert: {sourceFile} : {e}')
    
    msApp.Quit()

    return

#--------------------------------------------------------------------------------------------------

def main():

    import argparse

    parser = argparse.ArgumentParser(
        epilog=EPILOG, 
        description=DESCRIPTION, 
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-c', '--comobject',
        dest='comobject',
        type=str,
        default='Word.application',
        help="COM Object name of the application to be called. 'Word.application' or 'Excel.application'. Default, 'Word.application'."
    )
    parser.add_argument('-b', '--basedir',
        dest='basedir',
        type=Path,
        default=Path.home(),
        help='Directory to start the recursive scan from. Default, users HOME directory'
    )
    parser.add_argument('-s', '--srcext',
        dest='sourceextension',
        type=str,
        default='doc',
        help="File extension of the source files to be converted. Default, 'doc'."
    )
    parser.add_argument('-d', '--destext',
        dest='destinationextension',
        type=str,
        default='docx',
        help="File extension of the resulting converted file. Default, 'docx'."
    )
    parser.add_argument('-f', '--filefmt',
        dest='fileformat',
        type=int,
        default=16,
        help="Microsoft file format number of the output format. Default, 16."
    )
    parser.add_argument('--dryrun',
        dest='dryrun',
        action="store_true",
        default=False,
        help='Print out all files to be converter but do not carry out the actual conversion.'
    )

    args = parser.parse_args()

    converter(
        comObject=args.comobject,
        dirPath=args.basedir,
        sourceExtension=args.sourceextension,
        destinationExtension=args.destinationextension,
        fileFormat=args.fileformat,
        dryRun=args.dryrun
    )


#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    main()

#--------------------------------------------------------------------------------------------------