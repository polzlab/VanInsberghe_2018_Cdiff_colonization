#This script is functionally very similar to the count_spores.R, but with additional thresholding and filtering steps to increase accuracy of cell counts in fluorescent images from complex samples, like stool samples

library(EBImage)

countCells <- function(img_in){
  
  img_in[img_in < 0.015] <- 0 #This highpass threshold should be calibrated using images with known cell counts 
  #display(img_in, method = "raster")
  brush = makeBrush(7, shape='disc', step=FALSE)*0.2
  img_flo = filter2(img_in, brush)
  #display(img_flo, method = "raster")
  
  brush = matrix(1, nc=3, nr=3)
  brush[2,2] = -7
  img_filtered = filter2(img_flo, brush)
  #display(img_filtered, method = "raster")
  
  img_subtract = (imageData(img_flo)-imageData(img_filtered))
  img_subtract[img_subtract < 0] <- 0
  img_subtract = Image(img_subtract*5)
  #display(img_subtract, method = "raster")
  
  brush = makeBrush(3, shape='disc', step=FALSE)*0.3
  img_out = filter2(img_subtract, brush)
  #display(img_out, method = "raster")
  nmaskt = thresh(img_out, w=4, h=4, offset=0.126) #The offset value should be calibrated using images with known cell counts, and checked against known positives and negatives
  #display(nmaskt, method = "raster")#,all = TRUE)
  
  nucNo <- bwlabel(nmaskt)
  fts = computeFeatures.shape(nucNo)
  sarea = fts[1:nrow(fts)]
  cellNo = sum(sarea>18) #The area threshold should be calibrated using images with known cell counts, and checked against known positives and negatives
  
  return(cellNo)
}
