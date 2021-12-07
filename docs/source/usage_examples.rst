Usage Examples
==============

The example below shows how to create a new phosphomatics experiment, upload data and parameter files and run the initial data processing routine.

.. code-block:: python

    import phosphomaitcs.phosphomaitcs as pa

    # Instantiate phosphomatics with your API key
    exp = pa.Phosphomatics( key = 'YOUR_API_KEY')

    # start a new experiment
    # - this retrieves a new datasetToken unique to this experiment
    exp.startNewExperiment()

    # upload your experimental data
    exp.uploadExperimentalData('path_to_phospho_data.tsv')

    # upload parameter file for your analysis
    exp.uploadParameterSet('path_to_parameter_file.yaml')

    # call initial data processing routine
    exp.process()

    # print your datasetToken
    print(exp.getDataSetToken())

