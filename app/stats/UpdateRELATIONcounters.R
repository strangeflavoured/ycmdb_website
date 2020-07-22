library(DBI)
library(RMySQL)

args = commandArgs(trailingOnly=TRUE)

db = dbConnect(MySQL(), dbname=args[1], host=args[2], user=args[3], password=args[4])

# list all tables
list_tables <- dbListTables(db)
parts <- sapply(strsplit(list_tables, '_'),'[',1)
list_data_tables <- list_tables[parts !='META' & parts !='RELATION']
list_data_tables <- list_data_tables[!(list_data_tables %in% c("Table_Names","alembic_version", "FooTable"))] # practice table for Jonathan
list_tables <- list_tables[!(list_tables %in% c("Table_Names","alembic_version", "FooTable"))] # practice table for Jonathan

#### RELATION_publication stats
print("__________ Relation Publication ________________")
# get list all publications
query ="select Publication_Link, uniqueID from RELATION_Publication order by Publication_Link"
all_pubs <- dbGetQuery(db, query)

# get number of entries for each publication in each table
for (t in 1:length(list_data_tables)){
  query <- paste("SELECT Publication_Link, count(*) as n_data FROM ", list_data_tables[t], " GROUP BY Publication_Link")
  out <- dbGetQuery(db, query) 
  
  # entires that cannot be found in the RELATION table
  nomatch <- is.na(match((out$Publication_Link) , all_pubs$Publication_Link))
  if (any(nomatch)){
    print(paste("!!! No matching record found for the following publications in table ",list_data_tables[t],":"))
    print(out$Publication_Link[nomatch])
    out <- out[!nomatch,]
  }
  
  all_pubs[match((out$Publication_Link) , all_pubs$Publication_Link),list_data_tables[t]] = out$n_data
  
  #### write new counts into DB:
  # check existence ot the column for the current table
  query <- paste("select column_name FROM information_schema.columns where table_name = 'RELATION_Publication' and column_name = '",list_data_tables[t], "'",sep = "")
  iscol <- dbGetQuery(db, query)
  
  if (length(iscol)== 0){ # add a column to the db if not there yet, with all vales
    query <- paste("ALTER TABLE RELATION_Publication ADD ",list_data_tables[t], " Integer", sep = "")
    dbGetQuery(db, query)
    
    # compile the write query
    cases = paste(" WHEN '", counts$Publication_Link, "' THEN  '",counts$n_data ,"'", sep= "", collapse = "" )
    ins = paste(counts$Publication_Link,sep = "", collapse = "','")
    query = paste("  RELATION_Publication SET ",list_data_tables[t]," = CASE  Publication_Link ", cases , " ELSE ",list_data_tables[t]," END WHERE Publication_Link IN('",ins,"')", sep = "")
    dbGetQuery(db, query)
    
    print(paste0("!!! Added column and counts ",list_data_tables[t]," in the RELATION_Publication table"))
    
  } else {# update inidvidual col values if column is already there
    new_data = all_pubs[c("Publication_Link", list_data_tables[t])]
    new_data[is.na(new_data)] = 0
    query <- paste("SELECT Publication_Link, ",list_data_tables[t] ," FROM RELATION_Publication ORDER BY Publication_Link",sep = "")
    old_data <- dbGetQuery(db, query)


    # identify changes in the numbers (returns new values)
    changes <- (old_data[,1] != new_data[,1]) | (old_data[,2] != new_data[,2])
    changes[is.na(changes)] <- TRUE
    
    if (any(changes)){ # update all vals
      # update the changed entires in the DB:
      cases = paste(" WHEN '", new_data[changes, 1], "' THEN  '", new_data[changes, 2] ,"'", sep= "", collapse = "" )
      ins = paste(new_data[changes, 1],sep = "", collapse = "','")
      query = paste("UPDATE RELATION_Publication SET ",list_data_tables[t]," = CASE  Publication_Link ", cases , " ELSE ",list_data_tables[t]," END WHERE Publication_Link IN('",ins,"')", sep = "")
      dbGetQuery(db, query) 
      
      # print some info
      print(paste0("!!! Updated counts for ",list_data_tables[t]," in the RELATION_Publication table"))
      print( data.frame(Publication_Link = new_data[changes,1], 
                        old = old_data[changes,2], 
                        new = new_data[changes,2]))
      
    } else {
      print(paste0("No counts for ",list_data_tables[t]," changed in the RELATION_Publication table"))
    }
    
  }
}

# replace NA with 0
all_pubs[is.na(all_pubs)] = 0


# compile sum stats
pub_matrix <- all_pubs[,!(names(all_pubs) %in% c("uniqueID","Publication_Link"))]
all_pubs$n_datatypes <- apply(pub_matrix, 1, function(x){return(sum(x!=0))})
all_pubs$n_data <- rowSums(pub_matrix)

# drop strange entries (todo: resolve in DB)
print(paste("For the following publications no data is in the DB:"))
print(all_pubs[all_pubs$n_datatypes == 0,c("Publication_Link","uniqueID")])
# all_pubs <- all_pubs[all_pubs$n_datatypes != 0,]


#### RELATION_Medium stats ###################################
print("__________ Relation Medium ________________")
# get list all publications
query = paste( "SELECT Medium_ID, uniqueID FROM RELATION_Medium ORDER BY Medium_ID ")
all_media <- dbGetQuery(db, query) 


# get number of entries for each medium in each table
for (t in 1:length(list_data_tables)){
  ## get counts for each medium in the table
  query <- paste("SELECT Medium_ID, count(*) as n_data FROM ", list_data_tables[t], " GROUP BY Medium_ID")
  counts <- dbGetQuery(db, query) 
  
  ## print out the ones that cannot be matched to the relation table
  nomatch <- is.na(match((counts$Medium_ID) , all_media$Medium_ID))
  if (any(nomatch)){
    print(paste("!!! No matching record found for the following media in table ",list_data_tables[t],":"))
    print(counts$Medium_ID[nomatch])
    counts <- counts[!nomatch,] # remove the not matched ones from the list count
  }
  
  ## write the  ndata colum to the all_media df
  all_media[match((counts$Medium_ID) , all_media$Medium_ID),list_data_tables[t]] = counts$n_data
  
  #### write new counts into DB:
  # check existence ot the column for the current table
  query <- paste("select column_name FROM information_schema.columns where table_name = 'RELATION_Medium' and column_name = '",list_data_tables[t], "'",sep = "")
  iscol <- dbGetQuery(db, query)
  
  if (length(iscol)== 0){ # add a column to the db if not there yet, with all vales
    query <- paste("ALTER TABLE RELATION_Medium ADD ",list_data_tables[t], " Integer", sep = "")
    dbGetQuery(db, query)
    
    # compile the write query
    cases = paste(" WHEN '", counts$Medium_ID, "' THEN  '",counts$n_data ,"'", sep= "", collapse = "" )
    ins = paste(counts$Medium_ID,sep = "", collapse = "','")
    query = paste("UPDATE RELATION_Medium SET ",list_data_tables[t]," = CASE  Medium_ID ", cases , " ELSE ",list_data_tables[t]," END WHERE Medium_ID IN('",ins,"')", sep = "")
    dbGetQuery(db, query)
    
    print(paste0("!!! Added column and counts ",list_data_tables[t]," in the RELATION_Medium table"))
    
  } else {# update inidvidual col values if column is already there
    new_data = all_media[c("Medium_ID", list_data_tables[t])]
    new_data[is.na(new_data)] = 0
    query <- paste("SELECT Medium_ID, ",list_data_tables[t] ," FROM RELATION_Medium ORDER BY Medium_ID",sep = "")
    old_data <- dbGetQuery(db, query)

    
    # identify changes in the numbers (returns new values)
    changes <- (old_data[,1] != new_data[,1]) | (old_data[,2] != new_data[,2])
    changes[is.na(changes)] <- TRUE
    
    
    if (any(changes)){ # update all vals
      # update the changed entires in the DB:
      cases = paste(" WHEN '", new_data[changes, 1], "' THEN  '", new_data[changes, 2] ,"'", sep= "", collapse = "" )
      ins = paste(new_data[changes, 1],sep = "", collapse = "','")
    
      query = paste("UPDATE RELATION_Medium SET ",list_data_tables[t]," = CASE  Medium_ID ", cases , " ELSE ",list_data_tables[t]," END WHERE Medium_ID IN('",ins,"')", sep = "")
      dbGetQuery(db, query)
      
      # print some info
      print(paste0("!!! Updated counts for ",list_data_tables[t]," in the RELATION_Medium table"))
      print( data.frame(Medium_ID = new_data[changes,1], 
                        old = old_data[changes,2], 
                        new = new_data[changes,2]))
      
    } else {
      print(paste0("No counts for ",list_data_tables[t]," changed in the RELATION_Medium table"))
    }
    
  }
  
}

# replace NA with 0
all_media[is.na(all_media)] = 0

# compile sum stats
media_matrix <- all_media[,!(names(all_media) %in% c("uniqueID","Medium_ID"))]
all_media$n_datatypes <- apply(media_matrix, 1, function(x){return(sum(x!=0))})
all_media$n_data <- rowSums(media_matrix)

# drop strange entries (todo: resolve in DB)
print(paste("For the following media no data is in the DB:"))
print(all_media[all_media$n_datatypes == 0,c("Medium_ID","uniqueID")])
# all_media <- all_media[all_media$n_datatypes != 0,]

# # check the print out
#  query = paste("SELECT * FROM RELATION_Medium")
# out <- dbGetQuery(db,query)
# View(out)

#### RELATION_Strain stats ##############################
print("__________ Relation Strain ________________")
# get list all publications
query = paste( "SELECT Strain_ID, uniqueID FROM RELATION_Strain ORDER BY Strain_ID") 
all_strains <- dbGetQuery(db, query) 

# get number of entries for each strain  in each table
for (t in 1:length(list_data_tables)){
  query <- paste("SELECT Strain_ID, count(*) as n_data FROM ", list_data_tables[t], " GROUP BY Strain_ID")
  out <- dbGetQuery(db, query) 
  
  nomatch <- is.na(match((out$Strain_ID) , all_strains$Strain_ID))
  if (any(nomatch)){
    print(paste("!!! No matching record found for the following strains in table ",list_data_tables[t],":"))
    print(out$Strain_ID[nomatch])
    out <- out[!nomatch,]
  }
  
  all_strains[match((out$Strain_ID) , all_strains$Strain_ID),list_data_tables[t]] = out$n_data
  
  #### write new counts into DB:
  # check existence ot the column for the current table
  query <- paste("select column_name FROM information_schema.columns where table_name = 'RELATION_Strain' and column_name = '",list_data_tables[t], "'",sep = "")
  iscol <- dbGetQuery(db, query)
  
  if (length(iscol)== 0){ # add a column to the db if not there yet, with all vales
    query <- paste("ALTER TABLE RELATION_Strain ADD ",list_data_tables[t], " Integer", sep = "")
    dbGetQuery(db, query)
    
    # compile the write query
    cases = paste(" WHEN '", counts$Strain_ID, "' THEN  '",counts$n_data ,"'", sep= "", collapse = "" )
    ins = paste(counts$Strain_ID,sep = "", collapse = "','")
    query = paste("UPDATE RELATION_Strain SET ",list_data_tables[t]," = CASE  Strain_ID ", cases , " ELSE ",list_data_tables[t]," END WHERE Strain_ID IN('",ins,"')", sep = "")
    dbGetQuery(db, query)
    
    print(paste0("!!! Added column and counts ",list_data_tables[t]," in the RELATION_Strain table"))
    
  } else {# update inidvidual col values if column is already there
    new_data = all_strains[c("Strain_ID", list_data_tables[t])]
    new_data[is.na(new_data)] = 0
    query <- paste("SELECT Strain_ID, ",list_data_tables[t] ," FROM RELATION_Strain ORDER BY Strain_ID",sep = "")
    old_data <- dbGetQuery(db, query)

    
    # identify changes in the numbers (returns new values)
    changes <- (old_data[,1] != new_data[,1]) | (old_data[,2] != new_data[,2])
    changes[is.na(changes)] <- TRUE
    
    
    if (any(changes)){ # update all vals
      # update the changed entires in the DB:
      cases = paste(" WHEN '", new_data[changes, 1], "' THEN  '", new_data[changes, 2] ,"'", sep= "", collapse = "" )
      ins = paste(new_data[changes, 1],sep = "", collapse = "','")
      query = paste("UPDATE RELATION_Strain SET ",list_data_tables[t]," = CASE  Strain_ID ", cases , " ELSE ",list_data_tables[t]," END WHERE Strain_ID IN('",ins,"')", sep = "")
      dbGetQuery(db, query)
      
      # print some info
      print(paste0("!!! Updated counts for ",list_data_tables[t]," in the RELATION_Strain table"))
      print( data.frame(Strain_ID  = new_data[changes,1], 
                        old = old_data[changes,2], 
                        new = new_data[changes,2]))
      
    } else {
      print(paste0("No counts for ",list_data_tables[t]," changed in the RELATION_Strain table"))
    }
    
  }
}

# replace NA with 0
all_strains[is.na(all_strains)] = 0

# compile sum stats
strain_matrix <- all_strains[,!(names(all_strains) %in% c("uniqueID","Strain_ID"))]
all_strains$n_datatypes <- apply(strain_matrix, 1, function(x){return(sum(x!=0))})
all_strains$n_data <- rowSums(strain_matrix)

# drop strange entries (todo: resolve in DB)
print(paste("For the following strains no data is in the DB:"))
print(all_strains[all_strains$n_datatypes == 0,c("Strain_ID","uniqueID")])
# all_strains <- all_strains[all_strains$n_datatypes != 0,]