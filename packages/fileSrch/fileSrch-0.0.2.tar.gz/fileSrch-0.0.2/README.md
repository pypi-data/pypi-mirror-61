## FileSrch
This is a simple package to search for files

## Install
 `pip3 install fileSrch`

## Example

Below example will list all the pdf files in the folder

    from fileSrch import filelist`    
    folder_path = '/home/user/Documents'`
    pdf_files  = filelist.files(folderpath,'*.pdf')
    print(pdf_files)

