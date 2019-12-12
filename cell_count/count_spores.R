#This script is designed to count spores and cells from pure cultures imaged using phase contrast microscopy

library(EBImage)

countCells <- function(img_in){
  # blur the image
  brush = array(100, dim=c(3,3))
  brush = brush/sum(brush)
  img_flo = filter2(img_in, brush)
  #display(1.0-img_flo, method = "raster")
  
  # apply a threshold
  nmaskt = thresh(1.0-img_flo, w=3, h=3, offset=0.025) #The offset value should be calibrated using images with known cell counts, and checked against known positives and negatives
  #display(nmaskt, method = "raster")#,all = TRUE)
    
  nucNo <- bwlabel(nmaskt)
  fts = computeFeatures.shape(nucNo)
  sarea = fts[1:nrow(fts)]
  cellNo = sum(sarea>16) #The area threshold should be calibrated using images with known cell counts, and checked against known positives and negatives
  
  return(cellNo)
}
