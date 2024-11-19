import './Query2.css';
import React, { useState } from "react";

export default function Query2() {
  const [isFormVisible, setIsFormVisible] = useState(false);

  const toggleFormVisibility = () => {
    setIsFormVisible((prev) => !prev);
  };

  const [times, setTimes] = useState({
    startTime: "",
    endTime: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTimes((prevTimes) => ({
      ...prevTimes,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Start Time:", times.startTime);
    console.log("End Time:", times.endTime);
  };

  return (
    <div className='query2'>

      <div className='query2Box'>
        
        <div className='query2Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query2Desc'> Find the total number of reports per day for a specific “Crm Cd” and time range.</span>
        </div>

        <hr className='query2Line' />
        {isFormVisible && (
          <>
          <div className='query2Middle'>
            <form className='query2Form' onSubmit={handleSubmit}>
                <div className='startTime'>
                    <label htmlFor="startTime">Start Time</label>
                    <input className='startTimeInput' type="time" id="startTime" name="startTime" value={times.startTime} onChange={handleChange}/>
                </div>
                <div className='endTime'>
                    <label htmlFor="endTime">End Time</label>
                    <input className='endTimeInput' type="time" id="endTime" name="endTime" value={times.endTime} onChange={handleChange} />
                </div>
                
                  <div className='crmCDquery2'>
                      <label htmlFor="crmCD">Crm Cd</label>
                      <input className="crmCDquery2Input" list="numbers" id="numberInput" name="numberInput" placeholder="Select a Crm Cd"/>
                      <datalist id="numbers">
                                  <option value="110"></option>
                                  <option value="113"></option>
                                  <option value="121"></option>
                                  <option value="122"></option>
                                  <option value="210"></option>
                                  <option value="220"></option>
                                  <option value="230"></option>
                                  <option value="231"></option>
                                  <option value="235"></option>
                                  <option value="236"></option>
                                  <option value="237"></option>
                                  <option value="250"></option>
                                  <option value="251"></option>
                                  <option value="310"></option>
                                  <option value="320"></option>
                                  <option value="330"></option>
                                  <option value="331"></option>
                                  <option value="341"></option>
                                  <option value="343"></option>
                                  <option value="345"></option>
                                  <option value="347"></option>
                                  <option value="349"></option>
                                  <option value="350"></option>
                                  <option value="351"></option>
                                  <option value="352"></option>
                                  <option value="353"></option>
                                  <option value="354"></option>
                                  <option value="410"></option>
                                  <option value="420"></option>
                                  <option value="421"></option>
                                  <option value="432"></option>
                                  <option value="433"></option>
                                  <option value="434"></option>
                                  <option value="435"></option>
                                  <option value="436"></option>
                                  <option value="437"></option>
                                  <option value="438"></option>
                                  <option value="439"></option>
                                  <option value="440"></option>
                                  <option value="441"></option>
                                  <option value="442"></option>
                                  <option value="443"></option>
                                  <option value="444"></option>
                                  <option value="445"></option>
                                  <option value="446"></option>
                                  <option value="450"></option>
                                  <option value="451"></option>
                                  <option value="452"></option>
                                  <option value="453"></option>
                                  <option value="470"></option>
                                  <option value="471"></option>
                                  <option value="473"></option>
                                  <option value="474"></option>
                                  <option value="475"></option>
                                  <option value="480"></option>
                                  <option value="485"></option>
                                  <option value="487"></option>
                                  <option value="510"></option>
                                  <option value="520"></option>
                                  <option value="522"></option>
                                  <option value="622"></option>
                                  <option value="623"></option>
                                  <option value="624"></option>
                                  <option value="625"></option>
                                  <option value="626"></option>
                                  <option value="627"></option>
                                  <option value="647"></option>
                                  <option value="648"></option>
                                  <option value="649"></option>
                                  <option value="651"></option>
                                  <option value="652"></option>
                                  <option value="653"></option>
                                  <option value="654"></option>
                                  <option value="660"></option>
                                  <option value="661"></option>
                                  <option value="662"></option>
                                  <option value="664"></option>
                                  <option value="666"></option>
                                  <option value="668"></option>
                                  <option value="670"></option>
                                  <option value="740"></option>
                                  <option value="745"></option>
                                  <option value="753"></option>
                                  <option value="755"></option>
                                  <option value="756"></option>
                                  <option value="760"></option>
                                  <option value="761"></option>
                                  <option value="762"></option>
                                  <option value="763"></option>
                                  <option value="805"></option>
                                  <option value="806"></option>
                                  <option value="810"></option>
                                  <option value="812"></option>
                                  <option value="813"></option>
                                  <option value="814"></option>
                                  <option value="815"></option>
                                  <option value="820"></option>
                                  <option value="821"></option>
                                  <option value="822"></option>
                                  <option value="830"></option>
                                  <option value="840"></option>
                                  <option value="845"></option>
                                  <option value="850"></option>
                                  <option value="860"></option>
                                  <option value="865"></option>
                                  <option value="870"></option>
                                  <option value="880"></option>
                                  <option value="882"></option>
                                  <option value="884"></option>
                                  <option value="886"></option>
                                  <option value="888"></option>
                                  <option value="890"></option>
                                  <option value="900"></option>
                                  <option value="901"></option>
                                  <option value="902"></option>
                                  <option value="903"></option>
                                  <option value="904"></option>
                                  <option value="906"></option>
                                  <option value="910"></option>
                                  <option value="920"></option>
                                  <option value="921"></option>
                                  <option value="922"></option>
                                  <option value="924"></option>
                                  <option value="926"></option>
                                  <option value="928"></option>
                                  <option value="930"></option>
                                  <option value="931"></option>
                                  <option value="932"></option>
                                  <option value="933"></option>
                                  <option value="940"></option>
                                  <option value="942"></option>
                                  <option value="943"></option>
                                  <option value="944"></option>
                                  <option value="946"></option>
                                  <option value="948"></option>
                                  <option value="949"></option>
                                  <option value="950"></option>
                                  <option value="951"></option>
                                  <option value="954"></option>
                                  <option value="956"></option>
                              </datalist>
                            
                  </div>
            </form>
          </div>

          <div className='query2Down'>
            <button type="submit" className='query2SubmitButton'>Submit</button>
          </div>
          </>
        )}

      </div>

    </div>
  )
}
