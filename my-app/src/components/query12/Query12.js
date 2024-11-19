import './Query12.css';
import React, { useState } from "react";

export default function Query12() {
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
    <div className='query12'>
      <div className='query12Box'>
        <div className='query12Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query12Desc'>12. Find the number of division of records for crimes reported on the same day in different areas using the same weapon for a specific time range.</span>
        </div>
        <hr className='query12Line' />
        {isFormVisible && (
          <>
            <div className='query12Middle'>
              <form className='query12Form' onSubmit={handleSubmit}>
                <div className='startTime'>
                  <label htmlFor="startTime">Start Time</label>
                  <input className='startTimeInput' type="time" id="startTime" name="startTime" value={times.startTime} onChange={handleChange} />
                </div>
                <div className='endTime'>
                  <label htmlFor="endTime">End Time</label>
                  <input className='endTimeInput' type="time" id="endTime" name="endTime" value={times.endTime} onChange={handleChange} />
                </div>
              </form>
            </div>
            <div className='query12Down'>
              <button type="submit" className='query12SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
