import './Query13.css';
import React, { useState } from "react";

export default function Query13() {
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
    <div className='query13'>

      <div className='query13Box'>
        
        <div className='query13Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query13Desc'>13. Find the total number of reports per day for a specific “N” and time range.</span>
        </div>

        <hr className='query13Line' />
        {isFormVisible && (
          <>
          <div className='query13Middle'>
            <form className='query13Form' onSubmit={handleSubmit}>
                <div className='startTime'>
                    <label htmlFor="startTime">Start Time</label>
                    <input className='startTimeInput' type="time" id="startTime" name="startTime" value={times.startTime} onChange={handleChange}/>
                </div>
                <div className='endTime'>
                    <label htmlFor="endTime">End Time</label>
                    <input className='endTimeInput' type="time" id="endTime" name="endTime" value={times.endTime} onChange={handleChange} />
                </div>
                
                  <div className='Nquery13'>
                      <label htmlFor="N">N</label>
                      <input
                        className="Nquery13Input"
                        id="numberInput"
                        name="numberInput"
                        type="number"
                        placeholder="Enter a value > 0"
                        min="1"
                        onChange={(e) => {
                          const value = e.target.value;
                          if (value && parseInt(value) <= 0) {
                            alert("Please enter a positive integer greater than 0.");
                          }
                        }}
                      />
                  </div>
            </form>
          </div>

          <div className='query13Down'>
            <button type="submit" className='query13SubmitButton'>Submit</button>
          </div>
          </>
        )}

      </div>

    </div>
  )
}
