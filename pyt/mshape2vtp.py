import numpy as np


# ========================================================= #
# ===  mshape => vtp surface file convertor             === #
# ========================================================= #

def mshape2vtp( inpFile=None ):

    # ------------------------------------------------- #
    # --- [1] Load Data                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): inpFile = "out/mshape_0001.dat"
    with open( inpFile, "r" ) as f:
        Data = np.loadtxt( f )

    # ------------------------------------------------- #
    # --- [2] Data Clipping                         --- #
    # ------------------------------------------------- #
    index   = np.where( Data[:,5] == 1.0 )
    vtkData = Data[index]
    print( "[mshape2vtp]    Data.shape = {0} ".format(    Data.shape ) )
    print( "[mshape2vtp] vtkData.shape = {0} ".format( vtkData.shape ) )

    # ------------------------------------------------- #
    # --- [3] Data => vtk poly Data ( surface )     --- #
    # ------------------------------------------------- #
    import nkVTKRoutines.vtkDataConverter as cvt
    cvt.vtkDataConverter( vtkFile="out.vtp", Data=vtkData, tag="sample", DataType="point" )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    
    import nkUtilities.genArgs as gar
    args    = gar.genArgs()
    if ( args["integer"] is not None ):
        inpFile = "out/mshape_{0:04}.dat".format( args["integer"] )
    else:
        inpFile = "out/mshape_0000.dat"
        
    mshape2vtp( inpFile=inpFile )


    # ------------------------------------------------- #
    # --- test profile generation ( for debug )     --- #
    # ------------------------------------------------- #
    generate__testprofile = False
    if ( generate__testprofile ):

        import nkUtilities.equiSpaceGrid as esg
        x1MinMaxNum = [ 0.0, 1.0, 11 ]
        x2MinMaxNum = [ 0.0, 1.0, 11 ]
        ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                         returnType = "point" )
        Data        = np.zeros( (ret.shape[0],6) )
        Data[:,0]   = ret[:,0]
        Data[:,1]   = ret[:,1]
        Data[:,2]   = np.sqrt( ret[:,0]**2 + ret[:,1]**2 )
        index       = np.where( Data[:,2] < 1.0 )
        ( Data[:,5] )[index] = 1.0

        with open( inpFile, "w" ) as f:
            names   = [ "x{0}".format(i+1) for i in range( Data.shape[1] ) ]
            f.write( "# " + " ".join( names ) + "\n" )
            f.write( "# " + " ".join( [ str(i) for i in range( Data.shape[1] ) ] ) + "\n" )
            np.savetxt( f, Data )
        mshape2vtp( inpFile=inpFile )
    
