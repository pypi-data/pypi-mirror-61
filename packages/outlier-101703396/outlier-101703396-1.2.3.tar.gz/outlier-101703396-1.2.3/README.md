# outlier_remover
A outlier removal tool, removes outlier row-wise using z-score or InterQuartile Range method <br/>PyPI Project link <a href = "https://pypi.org/project/outlier-remover-csv/">here</a> 
<H2>Usage</H2>
Use below commands to install and use
<ul>
  <li><b>pip install outlier-remover-csv</b></li>
  <li><b>python3</b></li>
>>>from outlier import outlier<br/>
>>>t = outlier.outlier(input_filename,output_filename,[method])  
 </ul>method is optional. It can be "z_score" or "iqr", by default it is "iqr"<br/>
 e.g 1. t = outlier.outlier("mydata.csv","out.csv","z_score")<br/>
 e.g 2. t = outlier.outlier("mydata.csv","out.csv")
