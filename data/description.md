## Data requirements

This directory stores data only for analysis purpose.

`raw_data.zip` (or you can use unzipped folder instead) is the data that represents original measurements of a physical process recorded by a specific device. 
To use the data for the expert application it has to be converted to a single *.csv file. To use the file it has to be organized in next format:
* each row has to be represented single observation,
* at the first column has to be shown a class of state (bad/good),
* at the second column have to be shown condition state (good/not working something/not working something another),
* each row have to be the same size,

You can use `analysis/prepare_data.ipynb` notebook for conversion. Some snippets already provided in it. Follow the structure of the data conversion in it.

### Description of `raw_data.zip`

Every folder in the file represents single experiment with one state of module. Every file in each folder represents one engine cycle and have to be contain the same size of ticks. Every folder name represents state which means next:
* cylinder_1st_off_is0 - state of engine with not working cylinder (issue 0)
* cylinder_1st_off_is1 - state of engine with not working cylinder (issue 1)
* cylinder_2nd_off_is0 - state of engine with not working cylinder (issue 0)
* cylinder_2nd_off_is1 - state of engine with not working cylinder (issue 1)
* cylinder_3rd_off_is0 - state of engine with not working cylinder (issue 0)
* cylinder_4th_off_is0 - state of engine with not working cylinder (issue 0)
* cylinder_4th_off_is1 - state of engine with not working cylinder (issue 1)
* cylinder_5th_off_is0 - state of engine with not working cylinder (issue 0)
* cylinder_6th_off_is0 - state of engine with not working cylinder (issue 0)
* cylinder_6th_off_is1 - state of engine with not working cylinder (issue 1)
* good_0 - state of engine with good condition (etalon)
* good_1 - state of engine with good condition
* good_2 - state of engine with good condition
* good_3 - state of engine with good condition
* good_300kWt_0 - state of engine with good condition (higher power)
* good_300kWt_1 - state of engine with good condition (higher power)
* good_4 - state of engine with good condition
* good_5 - state of engine with good condition
