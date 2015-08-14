import ROOT as r

r.gROOT.SetBatch(0)

# find absolute boundaries of the scan
# in most inefficient way possible (inefficient => simpler => hopefully fewer typos)
def getHistMaxMinBins(h = None):

  xMin = h.GetNbinsX() # maximum possible minimum -- large dummy value
  yMin = h.GetNbinsY() # large dummy value
  xMax = 0
  yMax = 0

  for iX in range(1, h.GetNbinsX()+1):
    for iY in range(1, h.GetNbinsY()+1):
      if(h.GetBinContent(iX, iY) > 1e-10):
        if(iX<xMin): xMin=iX
        if(iY<yMin): yMin=iY
        if(iX>xMax): xMax=iX
        if(iY>yMax): yMax=iY

  return xMin, xMax, yMin, yMax

def alongDiagonal(h = None, iX = None, iY = None):
  # calculate three most "northwestern" neigbors
  sumNW = h.GetBinContent(iX, iY+1)+h.GetBinContent(iX-1, iY+1)+h.GetBinContent(iX-1, iY)
  # calculate three most "southeastern" neigbors
  sumSE = h.GetBinContent(iX, iY-1)+h.GetBinContent(iX+1, iY-1)+h.GetBinContent(iX+1, iY)
  # etc.
  sumSW = h.GetBinContent(iX, iY-1)+h.GetBinContent(iX-1, iY-1)+h.GetBinContent(iX-1, iY)
  sumNE = h.GetBinContent(iX, iY+1)+h.GetBinContent(iX+1, iY+1)+h.GetBinContent(iX+1, iY)

  if((sumNW==0 and sumSE!=0) or (sumNW!=0 and sumSE==0) or 
     (sumSW==0 and sumNE!=0) or (sumSW!=0 and sumNE==0)
     ): return True
  else: return False

# # Omit bins with even bin index.
# # Use for test in which known values are omitted
# # to determine bias from interpolation
# def omitEven(h = None):
#   for i in range(1, h.GetNbinsX()+1):
#     for j in range(1, h.GetNbinsY()+1):
#       if(i%2==0 or j%2==0) h.SetBinContent(i, j, 0.)
#   return h

# # Omit bins with odd bin index.
# # Use for test in which known values are omitted
# # to determine bias from interpolation
# def omitEven(h = None):
#   for i in range(1, h.GetNbinsX()+1):
#     for j in range(1, h.GetNbinsY()+1):
#       if((i+1)%2==0 or (j+1)%2==0) h.SetBinContent(i, j, 0.)
#   return h




def interpolate(hist = None, firstInterpolationDirection = ""):
  histCopy = hist.Clone()

  xStepPlus = 0
  xStepMinus = 0
  yStepPlus = 0
  yStepMinus = 0

  if(firstInterpolationDirection=="SW" or firstInterpolationDirection=="NE" or firstInterpolationDirection=="Santa Fe"):
    xStepPlus = 1
    xStepMinus = -1
    yStepPlus = 1
    yStepMinus = -1
  elif(firstInterpolationDirection=="NW" or firstInterpolationDirection=="SE"):
    xStepPlus = -1
    xStepMinus = 1
    yStepPlus = 1
    yStepMinus = -1
  elif(firstInterpolationDirection=="N" or firstInterpolationDirection=="S" or firstInterpolationDirection=="NS" or firstInterpolationDirection=="SN"):
    xStepPlus = 0
    xStepMinus = 0
    yStepPlus = 1
    yStepMinus = -1
  elif(firstInterpolationDirection=="E" or firstInterpolationDirection=="W" or firstInterpolationDirection=="EW" or firstInterpolationDirection=="WE"):
    xStepPlus = 1
    xStepMinus = -1
    yStepPlus = 0
    yStepMinus = 0
  else:
    # to avoid uninitialized variable warnings
    xStepPlus=0
    xStepMinus=0
    yStepPlus=0
    yStepMinus=0
    print "%s is not an allowed smearing first interpolation direction.\n Allowed first interpolation directions are SW (equivalently NE), SE (equivalently NW), NS, EW" % firstInterpolationDirection
    return 0

  # make temporary histograms to store the results of both steps
  hist_step1 = histCopy.Clone()
  hist_step1.Reset()
  hist_step2 = histCopy.Clone()
  hist_step2.Reset()

  nBinsX = histCopy.GetNbinsX()
  nBinsY = histCopy.GetNbinsY()

  xMin, xMax, yMin, yMax = getHistMaxMinBins(histCopy)

  for i in range(1, nBinsX+1):
    for j in range(1, nBinsY+1):
      
      # do not extrapolate outside the scan
      if(i<xMin or i>xMax or j<yMin or j>yMax): continue
      
      if(not alongDiagonal(histCopy, i,j)): #point is not along the diagonal
        binContent = histCopy.GetBinContent(i, j)
        binContentPlusStep = histCopy.GetBinContent(i+xStepPlus, j+yStepPlus)
        binContentMinusStep = histCopy.GetBinContent(i+xStepMinus, j+yStepMinus)
        nFilled = 0
        if(binContentPlusStep>0): nFilled += 1
        if(binContentMinusStep>0): nFilled += 1
        # if we are at an empty bin and there are neighbors
        # in specified direction with non-zero entries
        if(binContent==0 and nFilled>0):
          # average over non-zero entries
          binContent = (binContentPlusStep+binContentMinusStep)/nFilled
          hist_step1.SetBinContent(i,j,binContent)
      else: #point is along the diagonal; average SW-NE direction
        binContent = histCopy.GetBinContent(i, j)
        binContentPlusStep = histCopy.GetBinContent(i+1, j+1)
        binContentMinusStep = histCopy.GetBinContent(i-1, j-1)
        nFilled = 0
        if(binContentPlusStep>0): nFilled += 1
        if(binContentMinusStep>0): nFilled += 1
        # if we are at an empty bin and there are neighbors
        # in specified direction with non-zero entries
        if(binContent==0 and nFilled==2):
          # average over non-zero entries
          binContent = (binContentPlusStep+binContentMinusStep)/nFilled
          hist_step1.SetBinContent(i,j,binContent)
  
  # add result of interpolation
  histCopy.Add(hist_step1)

  for i in range(1, nBinsX+1):
    for j in range(1, nBinsY+1):
      if(i<xMin or i>xMax or j<yMin or j>yMax or alongDiagonal(histCopy, i,j)): continue
      binContent = histCopy.GetBinContent(i, j)
      # get entries for "Swiss Cross" average
      binContentUp = histCopy.GetBinContent(i, j+1)
      binContentDown = histCopy.GetBinContent(i, j-1)
      binContentLeft = histCopy.GetBinContent(i-1, j)
      binContentRight = histCopy.GetBinContent(i+1, j)
      nFilled=0
      if(binContentUp>0): nFilled += 1
      if(binContentDown>0): nFilled += 1
      if(binContentRight>0): nFilled += 1
      if(binContentLeft>0): nFilled += 1
      if(binContent==0 and nFilled>0):
        # only average over non-zero entries
        binContent = float((binContentUp+binContentDown+binContentRight+binContentLeft)/nFilled)
        hist_step2.SetBinContent(i,j,binContent)

  # add "Swiss Cross" average
  histCopy.Add(hist_step2)

  return histCopy


def rebin(hist = None, firstInterpolationDirection = ""):
  histName = hist.GetName()
  histName += "_rebin"

  print "> Rebinning hist..."

  # bin widths are needed so as to not shift histogram by half a bin with each rebinning
  # assume constant binning
  binWidthX = hist.GetXaxis().GetBinWidth(1)
  binWidthY = hist.GetYaxis().GetBinWidth(1)

  histRebinned = r.TH2F(histName, histName,
              2*hist.GetNbinsX(),
              hist.GetXaxis().GetXmin()+float(binWidthX/4.),
              hist.GetXaxis().GetXmax()+float(binWidthX/4.),
              2*hist.GetNbinsY(),
              hist.GetYaxis().GetXmin()+float(binWidthY/4.),
              hist.GetYaxis().GetXmax()+float(binWidthY/4.))

  # copy results from previous histogram
  for iX in range(1, hist.GetNbinsX()+1):
    for iY in range(1, hist.GetNbinsY()+1):
      binContent = hist.GetBinContent(iX, iY)
      histRebinned.SetBinContent(2*iX-1, 2*iY-1, binContent)
  histRebinned.SetMaximum(hist.GetMaximum())
  histRebinned.SetMinimum(hist.GetMinimum())

  # use interpolation to re-fill histogram
  histRebinnedInterpolated = interpolate(histRebinned, firstInterpolationDirection)
 
  return histRebinnedInterpolated

# def th2Smooth(hist = None):
#   if "TH2" not in type(hist):
#     print ">>> Warning: th2Smooth needs a TH2 root object. Returning..."
#     return
#   # Double_t k5a[5][5] =  { { 0, 0, 1, 0, 0 },
#   #                          { 0, 2, 2, 2, 0 },
#   #                          { 1, 2, 5, 2, 1 },
#   #                          { 0, 2, 2, 2, 0 },
#   #                          { 0, 0, 1, 0, 0 } };
#   #  Double_t k5b[5][5] =  { { 0, 1, 2, 1, 0 },
#   #                          { 1, 2, 4, 2, 1 },
#   #                          { 2, 4, 8, 4, 2 },
#   #                          { 1, 2, 4, 2, 1 },
#   #                          { 0, 1, 2, 1, 0 } };
#   k3a =  [ [ 0, 1, 0 ],
#            [ 1, 2, 1 ],
#            [ 0, 1, 0 ] ];


#   kernel = k3a
#   ksize_x=3
#   ksize_y=3


#   ifirst = hist.GetXaxis().GetFirst()
#   ilast  = hist.GetXaxis().GetLast()
#   jfirst = hist.GetYaxis().GetFirst()
#   jlast  = hist.GetYaxis().GetLast()

#   nentries = hist.GetEntries()
#   nx = hist.GetNbinsX()
#   ny = hist.GetNbinsY()
#   bufSize  = (nx+2)*(ny+2)
#   buf  = {};
#    # if (fSumw2.fN) ebuf = new Double_t[bufSize];

#   for i in range(1, nx+1):
#     for j in range(1, ny+1):
#       bin = hist.GetBin(i,j)
#       buf[bin] = hist.RetrieveBinContent(bin)
#          # if (ebuf) ebuf[bin]=GetBinError(bin);

#    # // Kernel tail sizes (kernel sizes must be odd for this to work!)
#   x_push = float((ksize_x-1)/2.)
#   y_push = float((ksize_y-1)/2.)

#   for i in range(1, nx+1):
#     for j in range(1, ny+1):
#       content = 0.0
#       error = 0.0
#       norm = 0.0
#       for n in range(ksize_x):
#         for m in range(ksize_y):
#           xb = i+(n-x_push)
#           yb = j+(m-y_push)
#           if ( (xb >= 1) and (xb <= nx) and (yb >= 1) and (yb <= ny) ):
#             bin = GetBin(xb,yb)
#             k = kernel[n*ksize_x][m]
#             if ( k != 0.0 ) {
#               norm    += k;
#               content += k*buf[bin];
#                      # if (ebuf) error   += k*k*ebuf[bin]*ebuf[bin];

#       if ( norm != 0.0 ):
#         hist.SetBinContent(i,j,content/norm)
#             # if (ebuf) {
#             #    error /= (norm*norm);
#             #    SetBinError(i,j,sqrt(error));
#             # }
#    fEntries = nentries;

#    # delete [] buf;
#    # delete [] ebuf;

if __name__ == "__main__":
  print ">>> Debugging smoother.py..."
  print ">   No syntax issues found."
