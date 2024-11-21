import './Query6.css'; 
import React, { useState } from "react";

export default function Query6() {
  const [isFormVisible, setIsFormVisible] = useState(false);

  const toggleFormVisibility = () => {
    setIsFormVisible((prev) => !prev);
  };

  const [dates, setDates] = useState({
    startDate: "",
    endDate: "",
  });

  const [category, setCategory] = useState("dateRange"); // Default επιλογή
  // const [rptDistNo, setRptDistNo] = useState(""); // 

  const handleDateChange = (e) => {
    const { name, value } = e.target;
    setDates((prevDates) => ({
      ...prevDates,
      [name]: value,
    }));
  };

  const handleCategoryChange = (e) => {
    setCategory(e.target.value);
  };

  // const handleRptChange = (e) => {
  //   setRptDistNo(e.target.value);
  // };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (category === "rptDistNo") {
      // console.log("Rpt Dist No:", rptDistNo);
    } else {
      console.log("Start Date:", dates.startDate);
      console.log("End Date:", dates.endDate);
    }
    console.log("Category:", category);
  };

  return (
    <div className='query6'>
      <div className='query6Box'>
        <div className='query6Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query6Desc'>6. Find the total number of crimes for a specific date range or a specific Rpt Dist No.</span>
        </div>
        <hr className='query6Line' />
        {isFormVisible && (
          <>
            <div className='query6Middle'>
              <form className='query6Form' onSubmit={handleSubmit}>
                <div className='categorySelect'>
                  <label htmlFor="category">Select Input Type:</label>
                  <select id="category" value={category} onChange={handleCategoryChange}>
                    <option value="dateRange">Date Range</option>
                    <option value="rptDistNo">Rpt Dist No</option>
                  </select>
                </div>

                {category === "dateRange" && (
                  <>
                    <div className='DateBoxQuery6'>
                        <div className='startDate'>
                        <label htmlFor="startDate">Start Date</label>
                        <input className='startDateInput' type="date" id="startDate" name="startDate" value={dates.startDate} onChange={handleDateChange}/>
                        </div>
                        <div className='endDate'>
                        <label htmlFor="endDate">End Date</label>
                        <input className='endDateInput' type="date" id="endDate" name="endDate" value={dates.endDate} onChange={handleDateChange}/>
                        </div>
                    </div>
                  </>
                )}

                {category === "rptDistNo" && (
                  <div className='rptDistInput'>
                    <label htmlFor="rptDistNo">Rpt Dist No</label>
                    <input className='rptDistInputField' list="numbersRpt" id="rptDistNo" name="rptDistNo" placeholder="Select a Rpt Dist No"/>
                    <datalist id="numbersRpt">
                        <option value="101"></option>
                        <option value="105"></option>
                        <option value="111"></option>
                        <option value="119"></option>
                        <option value="134"></option>
                        <option value="135"></option>
                        <option value="138"></option>
                        <option value="139"></option>
                        <option value="142"></option>
                        <option value="146"></option>
                        <option value="147"></option>
                        <option value="148"></option>
                        <option value="152"></option>
                        <option value="153"></option>
                        <option value="156"></option>
                        <option value="157"></option>
                        <option value="158"></option>
                        <option value="159"></option>
                        <option value="161"></option>
                        <option value="162"></option>
                        <option value="163"></option>
                        <option value="164"></option>
                        <option value="165"></option>
                        <option value="166"></option>
                        <option value="174"></option>
                        <option value="182"></option>
                        <option value="191"></option>
                        <option value="192"></option>
                        <option value="195"></option>
                        <option value="201"></option>
                        <option value="202"></option>
                        <option value="211"></option>
                        <option value="212"></option>
                        <option value="215"></option>
                        <option value="216"></option>
                        <option value="218"></option>
                        <option value="219"></option>
                        <option value="236"></option>
                        <option value="237"></option>
                        <option value="245"></option>
                        <option value="246"></option>
                        <option value="247"></option>
                        <option value="248"></option>
                        <option value="249"></option>
                        <option value="251"></option>
                        <option value="257"></option>
                        <option value="261"></option>
                        <option value="265"></option>
                        <option value="271"></option>
                        <option value="275"></option>
                        <option value="279"></option>
                        <option value="285"></option>
                        <option value="295"></option>
                        <option value="299"></option>
                        <option value="311"></option>
                        <option value="315"></option>
                        <option value="321"></option>
                        <option value="326"></option>
                        <option value="328"></option>
                        <option value="333"></option>
                        <option value="335"></option>
                        <option value="354"></option>
                        <option value="356"></option>
                        <option value="357"></option>
                        <option value="361"></option>
                        <option value="362"></option>
                        <option value="363"></option>
                        <option value="373"></option>
                        <option value="374"></option>
                        <option value="375"></option>
                        <option value="377"></option>
                        <option value="391"></option>
                        <option value="392"></option>
                        <option value="393"></option>
                        <option value="394"></option>
                        <option value="395"></option>
                        <option value="396"></option>
                        <option value="397"></option>
                        <option value="398"></option>
                        <option value="399"></option>
                        <option value="401"></option>
                        <option value="402"></option>
                        <option value="403"></option>
                        <option value="404"></option>
                        <option value="407"></option>
                        <option value="408"></option>
                        <option value="409"></option>
                        <option value="411"></option>
                        <option value="412"></option>
                        <option value="415"></option>
                        <option value="421"></option>
                        <option value="422"></option>
                        <option value="423"></option>
                        <option value="424"></option>
                        <option value="426"></option>
                        <option value="427"></option>
                        <option value="437"></option>
                        <option value="438"></option>
                        <option value="439"></option>
                        <option value="449"></option>
                        <option value="453"></option>
                        <option value="454"></option>
                        <option value="455"></option>
                        <option value="456"></option>
                        <option value="457"></option>
                        <option value="459"></option>
                        <option value="464"></option>
                        <option value="465"></option>
                        <option value="466"></option>
                        <option value="467"></option>
                        <option value="469"></option>
                        <option value="478"></option>
                        <option value="479"></option>
                        <option value="487"></option>
                        <option value="491"></option>
                        <option value="497"></option>
                        <option value="499"></option>
                        <option value="501"></option>
                        <option value="503"></option>
                        <option value="507"></option>
                        <option value="511"></option>
                        <option value="513"></option>
                        <option value="515"></option>
                        <option value="517"></option>
                        <option value="519"></option>
                        <option value="521"></option>
                        <option value="522"></option>
                        <option value="525"></option>
                        <option value="526"></option>
                        <option value="528"></option>
                        <option value="529"></option>
                        <option value="532"></option>
                        <option value="551"></option>
                        <option value="555"></option>
                        <option value="564"></option>
                        <option value="566"></option>
                        <option value="567"></option>
                        <option value="585"></option>
                        <option value="587"></option>
                        <option value="622"></option>
                        <option value="626"></option>
                        <option value="636"></option>
                        <option value="637"></option>
                        <option value="638"></option>
                        <option value="643"></option>
                        <option value="644"></option>
                        <option value="645"></option>
                        <option value="647"></option>
                        <option value="648"></option>
                        <option value="649"></option>
                        <option value="666"></option>
                        <option value="667"></option>
                        <option value="678"></option>
                        <option value="702"></option>
                        <option value="714"></option>
                        <option value="715"></option>
                        <option value="717"></option>
                        <option value="722"></option>
                        <option value="734"></option>
                        <option value="735"></option>
                        <option value="745"></option>
                        <option value="749"></option>
                        <option value="752"></option>
                        <option value="755"></option>
                        <option value="759"></option>
                        <option value="763"></option>
                        <option value="765"></option>
                        <option value="766"></option>
                        <option value="775"></option>
                        <option value="777"></option>
                        <option value="783"></option>
                        <option value="784"></option>
                        <option value="789"></option>
                        <option value="808"></option>
                        <option value="839"></option>
                        <option value="853"></option>
                        <option value="889"></option>
                        <option value="901"></option>
                        <option value="905"></option>
                        <option value="906"></option>
                        <option value="909"></option>
                        <option value="911"></option>
                        <option value="914"></option>
                        <option value="916"></option>
                        <option value="923"></option>
                        <option value="926"></option>
                        <option value="941"></option>
                        <option value="952"></option>
                        <option value="969"></option>
                        <option value="974"></option>
                        <option value="1003"></option>
                        <option value="1004"></option>
                        <option value="1006"></option>
                        <option value="1011"></option>
                        <option value="1018"></option>
                        <option value="1029"></option>
                        <option value="1035"></option>
                        <option value="1039"></option>
                        <option value="1045"></option>
                        <option value="1047"></option>
                        <option value="1063"></option>
                        <option value="1079"></option>
                        <option value="1094"></option>
                        <option value="1097"></option>
                        <option value="1102"></option>
                        <option value="1118"></option>
                        <option value="1124"></option>
                        <option value="1125"></option>
                        <option value="1127"></option>
                        <option value="1134"></option>
                        <option value="1136"></option>
                        <option value="1137"></option>
                        <option value="1138"></option>
                        <option value="1139"></option>
                        <option value="1145"></option>
                        <option value="1148"></option>
                        <option value="1151"></option>
                        <option value="1162"></option>
                        <option value="1173"></option>
                        <option value="1176"></option>
                        <option value="1177"></option>
                        <option value="1178"></option>
                        <option value="1181"></option>
                        <option value="1184"></option>
                        <option value="1203"></option>
                        <option value="1204"></option>
                        <option value="1207"></option>
                        <option value="1208"></option>
                        <option value="1211"></option>
                        <option value="1213"></option>
                        <option value="1215"></option>
                        <option value="1218"></option>
                        <option value="1232"></option>
                        <option value="1233"></option>
                        <option value="1235"></option>
                        <option value="1239"></option>
                        <option value="1243"></option>
                        <option value="1245"></option>
                        <option value="1248"></option>
                        <option value="1249"></option>
                        <option value="1251"></option>
                        <option value="1252"></option>
                        <option value="1253"></option>
                        <option value="1255"></option>
                        <option value="1256"></option>
                        <option value="1258"></option>
                        <option value="1259"></option>
                        <option value="1263"></option>
                        <option value="1265"></option>
                        <option value="1266"></option>
                        <option value="1267"></option>
                        <option value="1268"></option>
                        <option value="1269"></option>
                        <option value="1273"></option>
                        <option value="1283"></option>
                        <option value="1303"></option>
                        <option value="1307"></option>
                        <option value="1309"></option>
                        <option value="1317"></option>
                        <option value="1321"></option>
                        <option value="1323"></option>
                        <option value="1324"></option>
                        <option value="1331"></option>
                        <option value="1333"></option>
                        <option value="1341"></option>
                        <option value="1342"></option>
                        <option value="1343"></option>
                        <option value="1344"></option>
                        <option value="1347"></option>
                        <option value="1351"></option>
                        <option value="1352"></option>
                        <option value="1353"></option>
                        <option value="1361"></option>
                        <option value="1362"></option>
                        <option value="1363"></option>
                        <option value="1367"></option>
                        <option value="1371"></option>
                        <option value="1372"></option>
                        <option value="1373"></option>
                        <option value="1375"></option>
                        <option value="1377"></option>
                        <option value="1383"></option>
                        <option value="1385"></option>
                        <option value="1391"></option>
                        <option value="1393"></option>
                        <option value="1394"></option>
                        <option value="1395"></option>
                        <option value="1409"></option>
                        <option value="1411"></option>
                        <option value="1412"></option>
                        <option value="1414"></option>
                        <option value="1425"></option>
                        <option value="1431"></option>
                        <option value="1432"></option>
                        <option value="1445"></option>
                        <option value="1458"></option>
                        <option value="1468"></option>
                        <option value="1472"></option>
                        <option value="1484"></option>
                        <option value="1488"></option>
                        <option value="1504"></option>
                        <option value="1506"></option>
                        <option value="1513"></option>
                        <option value="1514"></option>
                        <option value="1515"></option>
                        <option value="1519"></option>
                        <option value="1521"></option>
                        <option value="1522"></option>
                        <option value="1525"></option>
                        <option value="1529"></option>
                        <option value="1532"></option>
                        <option value="1538"></option>
                        <option value="1547"></option>
                        <option value="1549"></option>
                        <option value="1553"></option>
                        <option value="1555"></option>
                        <option value="1583"></option>
                        <option value="1585"></option>
                        <option value="1591"></option>
                        <option value="1601"></option>
                        <option value="1602"></option>
                        <option value="1611"></option>
                        <option value="1613"></option>
                        <option value="1621"></option>
                        <option value="1622"></option>
                        <option value="1623"></option>
                        <option value="1633"></option>
                        <option value="1641"></option>
                        <option value="1653"></option>
                        <option value="1664"></option>
                        <option value="1684"></option>
                        <option value="1685"></option>
                        <option value="1693"></option>
                        <option value="1745"></option>
                        <option value="1749"></option>
                        <option value="1762"></option>
                        <option value="1764"></option>
                        <option value="1781"></option>
                        <option value="1782"></option>
                        <option value="1793"></option>
                        <option value="1797"></option>
                        <option value="1799"></option>
                        <option value="1801"></option>
                        <option value="1802"></option>
                        <option value="1803"></option>
                        <option value="1804"></option>
                        <option value="1805"></option>
                        <option value="1806"></option>
                        <option value="1821"></option>
                        <option value="1822"></option>
                        <option value="1823"></option>
                        <option value="1824"></option>
                        <option value="1826"></option>
                        <option value="1827"></option>
                        <option value="1829"></option>
                        <option value="1831"></option>
                        <option value="1834"></option>
                        <option value="1836"></option>
                        <option value="1837"></option>
                        <option value="1838"></option>
                        <option value="1839"></option>
                        <option value="1841"></option>
                        <option value="1842"></option>
                        <option value="1844"></option>
                        <option value="1846"></option>
                        <option value="1849"></option>
                        <option value="1851"></option>
                        <option value="1861"></option>
                        <option value="1862"></option>
                        <option value="1863"></option>
                        <option value="1864"></option>
                        <option value="1871"></option>
                        <option value="1891"></option>
                        <option value="1902"></option>
                        <option value="1907"></option>
                        <option value="1913"></option>
                        <option value="1915"></option>
                        <option value="1916"></option>
                        <option value="1918"></option>
                        <option value="1921"></option>
                        <option value="1954"></option>
                        <option value="1961"></option>
                        <option value="1962"></option>
                        <option value="1967"></option>
                        <option value="1971"></option>
                        <option value="1972"></option>
                        <option value="1979"></option>
                        <option value="1982"></option>
                        <option value="1984"></option>
                        <option value="1988"></option>
                        <option value="1991"></option>
                        <option value="1994"></option>
                        <option value="1995"></option>
                        <option value="1998"></option>
                        <option value="1999"></option>
                        <option value="2001"></option>
                        <option value="2004"></option>
                        <option value="2011"></option>
                        <option value="2015"></option>
                        <option value="2017"></option>
                        <option value="2021"></option>
                        <option value="2026"></option>
                        <option value="2027"></option>
                        <option value="2036"></option>
                        <option value="2039"></option>
                        <option value="2042"></option>
                        <option value="2046"></option>
                        <option value="2049"></option>
                        <option value="2058"></option>
                        <option value="2062"></option>
                        <option value="2064"></option>
                        <option value="2069"></option>
                        <option value="2076"></option>
                        <option value="2081"></option>
                        <option value="2091"></option>
                        <option value="2113"></option>
                        <option value="2126"></option>
                        <option value="2139"></option>
                        <option value="2142"></option>
                        <option value="2144"></option>
                        <option value="2146"></option>
                        <option value="2148"></option>
                        <option value="2155"></option>
                        <option value="2157"></option>
                        <option value="2158"></option>
                        <option value="2177"></option>
                        <option value="2183"></option>
                        <option value="2189"></option>
                    </datalist>
                  </div>
                )}
              </form>
            </div>
            <div className='query6Down'>
              <button type="submit" className='query6SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
