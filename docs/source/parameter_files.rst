Parameter Files
===============

Phosphomatics uses a yaml-style parameter file to configure initial data processing and track the creation of phosphorylation site data groups. The parameter file can be opened and edited in any plain text editor, or, alternatively, in python using the yaml library. An example parameter data file can be downloaded `here <https://www.phosphomatics.com>`_ and the text is copied at the end of this page.

Structure
---------

The minimal parameter file that can be used for initial processing of data consists of three blocks; columnAssignments, comparisons and processing. The order of these blocks is not important.

Column Assignments Block
^^^^^^^^^^^^^^^^^^^^^^^^
The column assignments block contains information about how individual columns from a larger data file are to be utilised for analysis. This section consists of 7 sub sections.

We must specify which columns are to be used for protein identifiers, phosphorylation site and residue specification as well as quantitative data. An example of these sections is below::

  upidColumn: <COLUMN_FOR_PROTEIN_UNIPROT_ID>
  residueColumn: <COLUMN_FOR_PHOSPHORYLATED_RESIDUE_(S/T/Y)>
  siteColumn: <COLUMN_FOR_PHOSPHORYLATION_POSITION_IN_PROTEIN>
  quantColumns:
  - <COLUMN_FOR_SAMPLE_1_QUANT_DATA>
  - <COLUMN_FOR_SAMPLE_2_QUANT_DATA>
    ...
  - <COLUMN_FOR_SAMPLE_X_QUANT_DATA>

For example, using the phosphomatics example data, this section would be::

  upidColumn: ID
  residueColumn: Residue
  siteColumn: Position
  quantColumns:
  - CTRL
  - CTRL_1
  - CTRL_2
  - THZ1
  - THZ1_1
  - THZ1_2
  - U0126
  - U0126_1
  - U0126_2

The ``sampleAliasMap`` block allows you to specify an alias for quantitation columns. This can be useful since many proteomics search software label these columns with the raw mass spectrometry data file name which is frequently long and verbose. Here, we alias columns in the original input files ('QUANT_CTRL', 'QUANT_CTRL_1'...) to 'CTRL', 'CTRL_1' which removes the unnecessary 'QUANT_' prefix::

  sampleAliasMap:
    QUANT_CTRL: CTRL
    QUANT_CTRL_1: CTRL_1
    QUANT_CTRL_2: CTRL_2
    QUANT_THZ1: THZ1
    QUANT_THZ1_1: THZ1_1
    QUANT_THZ1_2: THZ1_2
    QUANT_U0126: U0126
    QUANT_U0126_1: U0126_1
    QUANT_U0126_2: U0126_2

The next section allows us to specify which samples correspond to which treatment groups. We've created three treatment groups called ``CTRL``, ``THZ1`` and ``U0126``::

  sampleGroupMap:
    CTRL: CTRL
    CTRL_1: CTRL
    CTRL_2: CTRL
    THZ1: THZ1
    THZ1_1: THZ1
    THZ1_2: THZ1
    U0126: U0126
    U0126_1: U0126
    U0126_2: U0126

The last section allows us to control the order in which data is presented. For example, with time series data, we usually want to plot/tabulate data in order of increasing time post-treatment. In the block below, indices can be entered beside individual files (1,2,3...) and the data will then be displayed with the specified order. The sample indexed 1 will be presented left most and the highest index will be presented right-most.::

  sampleIndexMap:
    CTRL: 1
    CTRL_1: 2
    CTRL_2: 3
    THZ1: 4
    THZ1_1: 5
    THZ1_2: 6
    U0126: 7
    U0126_1: 8
    U0126_2: 9

Comparisons Block
^^^^^^^^^^^^^^^^^^^^^^^^
ToDo

Processing Block
^^^^^^^^^^^^^^^^^^^^^^^^
ToDo

Example Parameter File
----------------------

An example parameter data file can be downloaded `here <https://www.phosphomatics.com>`_ and the text is copied below::

    columnAssignments:
      quantColumns:
      - CTRL
      - CTRL_1
      - CTRL_2
      - THZ1
      - THZ1_1
      - THZ1_2
      - U0126
      - U0126_1
      - U0126_2
      residueColumn: Residue
      sampleAliasMap:
        QUANT_CTRL: CTRL
        QUANT_CTRL_1: CTRL_1
        QUANT_CTRL_2: CTRL_2
        QUANT_THZ1: THZ1
        QUANT_THZ1_1: THZ1_1
        QUANT_THZ1_2: THZ1_2
        QUANT_U0126: U0126
        QUANT_U0126_1: U0126_1
        QUANT_U0126_2: U0126_2
      sampleGroupMap:
        CTRL: CTRL
        CTRL_1: CTRL
        CTRL_2: CTRL
        THZ1: THZ1
        THZ1_1: THZ1
        THZ1_2: THZ1
        U0126: U0126
        U0126_1: U0126
        U0126_2: U0126
      sampleIndexMap:
        CTRL: 1
        CTRL_1: 2
        CTRL_2: 3
        THZ1: 4
        THZ1_1: 5
        THZ1_2: 6
        U0126: 7
        U0126_1: 8
        U0126_2: 9
      siteColumn: Position
      upidColumn: ID
    comparisons:
    - foldChangeThreshold: '1'
      group1: THZ1
      group2: CTRL
      name: THZ1_CTRL
      pvalThreshold: '2'
    - foldChangeThreshold: '1'
      group1: U0126
      group2: CTRL
      name: U0126_CTRL
      pvalThreshold: '2'
    processing:
      filtering:
        doFiltering: 'false'
        filterTerms: []
        minValues: ''
        minValuesIn: group
      imputation:
        doImputation: 'false'
        imputeCategory: group
        imputeType: median
      normalisation: median
      transform: log2



