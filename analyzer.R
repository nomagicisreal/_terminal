#
#
# most of the errors should be handled in python
#
#
library('haven')
suppressPackageStartupMessages(library('gdata'))


# 
# 
# available file types
# 
# 
fileTypeAvailables <- c('csv', 'sav')
infoFileTypeAvailable <- paste(
  'available file types:\n\n',
  paste(
    '\t',
    paste(1:length(fileTypeAvailables), fileTypeAvailables, sep = '.'),
    '\n',
    collapse = ''
  ),
  '\n'
)

#
#
# start looping until user provide the correct file path
#
#
fileType <- commandArgs(trailingOnly = TRUE)[1]

unfinished <- TRUE
while (unfinished) {
  # 
  # input file path or '..' to choose the file reader
  # 
  cat(paste('your', fileType, 'file location: '))
  input <- trim(readLines(con = 'stdin', n = 1))
  
  tryCatch({
    
    # 
    # 
    # choose file type
    # 
    # 
    if (input == '..') {
      notBeenChoosen <- TRUE
      cat(infoFileTypeAvailable)
      while (notBeenChoosen) {
        # 
        # input the index of file type
        # 
        cat('your options (index only): ')
        input <- trim(readLines(con = 'stdin', n = 1))
        
        tryCatch({
          fileType <- fileTypeAvailables[as.numeric(input)]
          if (is.na(fileType)) stop(paste('unknown', input))
          
          notBeenChoosen <- FALSE
        }
        ,error = function(e) cat(e$message, '\n')
        ,warning = function(e) cat(e$message, '\n')
        )
      }
      
    # 
    # 
    # provide file path
    # 
    # 
    } else {
      df <- switch(fileType,
         sav = read_sav(input),
         csv = read.csv(input),
      )
      if (is.null(df)) stop(paste('unimplement file type:', fileType))
      
      unfinished <- FALSE
    }
  }
  ,warning = function(e) cat(e$message, '\n')
  ,error = function(e) cat(e$message, '\n')
  )
}

cat(path, ' found!\n')
df
