
#####
# Step 3 - Make your own Python Toolbox!
#####

# Task - Using the code I provide below (basically , including the parameters that I have prepared for you (note, you can
# find all the Python Toolbox Parameters here:
# http://desktop.arcgis.com/en/arcmap/10.3/analyze/creating-tools/defining-parameters-in-a-python-toolbox.htm)

# I want you to attempt to construct a working Python Toolbox. Hint the code is the same as we used before for the
# traditional toolbox, however, I have changed how the arguements are provided to the tool.

# Code for parameters function
import arcpy
from arcpy.sa import *
arcpy.env.overwriteOutput = True

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "NDVI, DSM, and DHM Creator"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [NDVI_Calculator, DSM_Creator_Tool, DHM_Creator_Tool]

class NDVI_Calculator(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "NDVI_Calculator"
        self.description = ""
        self.canRunInBackground = False

    arcpy.env.overwriteOutput = True
    def getParameterInfo(self):
        params = []
        Input_Band4 = arcpy.Parameter(name="Input_Band4_or_Vis_Red",
                                     displayName="Input Band 4 or Vis Red",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # Input_Band4.value = r"D:\LC08_L1TP_012031_20150201_20170301_01_T1_B4.tif" # This is a default value that can be over-ridden in the toolbox
        params.append(Input_Band4)

        Input_Band5 = arcpy.Parameter(name="Input_Band5_or_NIR",
                                        displayName="Input Band 5 or NIR",
                                        datatype="DERasterDataset",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        # Input_Band5.value = r"D:\LC08_L1TP_012031_20150201_20170301_01_T1_B5.tif" # This is a default value that can be over-ridden in the toolbox
        params.append(Input_Band5)

        NDVI_Output = arcpy.Parameter(name="NDVI_Output",
                                 displayName="NDVI Output",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # NDVI_Output.value = r"D:\NDVI1.tif" # This is a default value that can be over-ridden in the toolbox
        params.append(NDVI_Output)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        # Code for execution function
        Input_Band4 = parameters[0].valueAsText
        Input_Band5 = parameters[1].valueAsText
        NDVI_Output = parameters[2].valueAsText

        expression = "(Float('{0}') - Float('{1}')) / (Float('{0}') + Float('{1}'))".format(Input_Band5, Input_Band4)
        arcpy.gp.RasterCalculator_sa(expression, NDVI_Output)

class DSM_Creator_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DSM_Creator_Tool"
        self.description = ""
        self.canRunInBackground = False

    arcpy.env.overwriteOutput = True
    def getParameterInfo(self):
        params = []
        Input_LAS_DSM = arcpy.Parameter(name="Input_LAS",
                                     displayName="Input LAS",
                                     datatype="DELasDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # Input_LAS_DSM.value = r"D:\19_02884594.las" # This is a default value that can be over-ridden in the toolbox
        params.append(Input_LAS_DSM)

        Cellsize = arcpy.Parameter(name="Cellsize",
                                        displayName="Cellsize",
                                        datatype="GPType",
                                        parameterType="Optional",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        Cellsize.value = "1" # This is a default value that can be over-ridden in the toolbox
        params.append(Cellsize)

        Output_DSM = arcpy.Parameter(name="Las_to_DSM",
                                 displayName="Output LAS to DSM",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # Output_DSM.value = r"D:\DSM2tools.tif" # This is a default value that can be over-ridden in the toolbox
        params.append(Output_DSM)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        # Code for execution function
        Input_LAS_DSM = parameters[0].valueAsText
        Cellsize = parameters[1].valueAsText
        Output_DSM = parameters[2].valueAsText

        arcpy.conversion.LasDatasetToRaster(in_las_dataset=Input_LAS_DSM,
                                            out_raster=Output_DSM,
                                            value_field="ELEVATION",
                                            interpolation_type="BINNING MAXIMUM LINEAR",
                                            data_type="FLOAT", sampling_type="CELLSIZE",
                                            sampling_value=Cellsize, z_factor=1)

class DHM_Creator_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DHM_Creator_Tool"
        self.description = ""
        self.canRunInBackground = False

    arcpy.env.overwriteOutput = True
    def getParameterInfo(self):
        params = []
        Input_LASDSM = arcpy.Parameter(name="Input_LAS",
                                     displayName="Input LAS",
                                     datatype="DELasDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # Input_LASDSM.value = r"D:\19_02884594.las" # This is a default value that can be over-ridden in the toolbox
        params.append(Input_LASDSM)

        Input_DEM = arcpy.Parameter(name="Input_DEM",
                                     displayName="Input DEM",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # Input_DEM.value = r"D:\19_02884594.img" # This is a default value that can be over-ridden in the toolbox
        params.append(Input_DEM)

        Cellsize = arcpy.Parameter(name="Cellsize",
                                        displayName="Cellsize",
                                        datatype="GPType",
                                        parameterType="Optional",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        Cellsize.value = "1" # This is a default value that can be over-ridden in the toolbox
        params.append(Cellsize)

        Output_DSM = arcpy.Parameter(name="Output_LAS_to_DSM.img",
                                 displayName="Output LAS to DSM (.img)",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # Output_DSM.value = r"D:\DSM.img" # This is a default value that can be over-ridden in the toolbox
        params.append(Output_DSM)

        Output_DHM = arcpy.Parameter(name="Output_LAS_to_DHM.img",
                                 displayName="Output LAS to DHM (.img)",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # Output_DHM.value = r"D:\DHM3tools.img" # This is a default value that can be over-ridden in the toolbox
        params.append(Output_DHM)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        # Code for execution function
        Input_LAS_DSM = parameters[0].valueAsText
        Input_DEM = parameters[1].valueAsText
        Cellsize = parameters[2].valueAsText
        Output_DSM = parameters[3].valueAsText
        Output_DHM = parameters[4].valueAsText

        arcpy.conversion.LasDatasetToRaster(in_las_dataset=Input_LAS_DSM,
                                            out_raster=Output_DSM,
                                            value_field="ELEVATION",
                                            interpolation_type="BINNING MAXIMUM LINEAR",
                                            data_type="FLOAT", sampling_type="CELLSIZE",
                                            sampling_value=Cellsize, z_factor=1)
        if arcpy.Exists(Output_DSM):
            outMinus = Minus(Output_DSM, Input_DEM)
            outMinus.save(Output_DHM)