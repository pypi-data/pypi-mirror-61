# pySDI
Thanks for your interest in **pySDI**. This is a free, open source code to compute univariated and multivariated nonparametric *Standardized Drought Indices* (SDI) following the methodology proposed by McKee *et al.* (1993), and  extended by Farahmand & AghaKouchak (2015), using raster maps as data source. It has been designed to use the land surface diagnosis data files of the NASA's atmospheric reanalysis product MERRA-2 (Modern-Era Reanalysis for Research and Applications, version 2; Gelaro et al., 2017) but future versions will allow to use other datasources (such as GLDAS-2; Rodell et al., 2004).

This project was originally developed as part of the Master in Engineering (Hydraulics) final project *Monitoreo de sequías en México a través de índices multivariados* [Drought monitoring in Mexico by mean of multivariated indices], developed in the Institute of Engineering of the National Autonomous University of Mexico (II-UNAM).

Currently, the documentation is still in development. Please, contact Roberto A. Real-Rangel (rrealr@iingen.unam.mx) for more information or support. This is an ongoing work. Any comments, suggestions or bugs reports will be appreciated.

## Main source of the project
The project repository is available at https://bitbucket.org/pysdi/pysdi.

## Installation
Write the following line in a terminal:
pip install [repository local path]

Additionally, you'll need to install the GDAL library through:
pip install GDAL

## Python dependencies
Required Python packages:
* gdal
* numpy
* pathlib2
* scipy
* sys
* toml
* warnings
* xarray

## Features in development
 - Drought forecasting using a multivariated linear regression approach.

## References
* Farahmand, A., & AghaKouchak, A. (2015). A generalized framework for deriving nonparametric standardized drought indicators. Advances in Water Resources, 76, 140–145. https://doi.org/10.1016/j.advwatres.2014.11.012
* Gelaro, R., McCarty, W., Suárez, M. J., Todling, R., Molod, A., Takacs, L., … Zhao, B. (2017). The Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2). Journal of Climate, 30(14), 5419–5454. https://doi.org/10.1175/JCLI-D-16-0758.1
* McKee, T. B., Doesken, N. J., & Kleist, J. (1993). The relationship of drought frequency and duration to time scales. In Eighth Conference on Applied Climatology (pp. 179–184). American Meteorological Society.
* Rodell, M., Houser, P. R., Jambor, U., Gottschalck, J., Mitchell, K. E., Meng, C.-J., … Toll, D. (2004). The Global Land Data Assimilation System. Bulletin of the American Meteorological Society, 85(3), 381–394. https://doi.org/10.1175/BAMS-85-3-381

## Publications
* Real-Rangel, Roberto Alejandro. (2016). _Monitoreo de sequías en México a través de índices multivariados_ [Master Thesis, Universidad Nacional Autónoma de México]. http://oreon.dgbiblio.unam.mx/F/26RGSMDMG66D3MCT844UJ8B7PNM9TDC8UVYB4S9N7ND1HBQ9TQ-27197?func=full-set-set&set_number=006474&set_entry=000001&format=999.

* Real-Rangel, Roberto A., Pedrozo-Acuña, A., Breña Naranjo, J. A., & Alcocer-Yamanaka, V. H. (2017, March). _Monitorización de sequías en México a través del Índice Estandarizado Multivariado de Sequía_. XXIV Congreso Nacional de Hidráulica, Acapulco, México.

* Real-Rangel, Roberto A., Pedrozo-Acuña, A., Breña-Naranjo, J. A., & Alcocer-Yamanaka, V. H. (2017). _An extended multivariate framework for drought monitoring in Mexico_. European Geophysics Union General Assembly 2017, Vienna, Austria.

* Real-Rangel, Roberto Alejandro, Pedrozo-Acuña, A., Breña-Naranjo, J. A., Alcocer-Yamanaka, V. H., & Ocón-Gutiérrez, A. R. (2017, December 11). _An improvement of drought monitoring through the use of a multivariate magnitude index_. AGU Fall Meeting 2017, New Orleans, LA.

* Real-Rangel, Roberto A., Pedrozo-Acuña, A., Breña-Naranjo, J. A., & Alcocer-Yamanaka, V. H. (2018). Novel Drought Hazard Monitoring Framework for Decision Support Under Data Scarcity. In G. La Loggia, G. Freni, V. Puleo, & M. D. Marchis (Eds.), _HIC 2018. 13th International Conference on Hydroinformatics_ (Vol. 3, pp. 1744–1751). EasyChair. https://doi.org/10.29007/1l5w

* Real-Rangel, Roberto A., Pedrozo-Acuña, A., Breña-Naranjo, J. A., & Alcocer-Yamanaka, V. H. (2020). A drought monitoring framework for data-scarce regions. _Journal of Hydroinformatics, 22_(1), 170–185. https://doi.org/10.2166/hydro.2019.020

# Author
Roberto A. Real-Rangel. Institute of Engineering of the National Autonomous University of Mexico (II-UNAM). rrealr@iingen.unam.mx.
