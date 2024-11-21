import './Query1.css';
import React, { useState } from "react";

export default function Query1() {
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
    <div className='query1'>
      <div className='query1Box'>
        <div className='query1Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query1Desc'>1. Find the total number of reports per “Crm Cd” that occurred within a specified time range and sort them in a descending order.</span>
        </div>
        <hr className='query1Line' />
        {isFormVisible && (
          <>
            <div className='query1Middle'>
              <form className='query1Form' onSubmit={handleSubmit}>
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
            <div className='query1Down'>
              <button type="submit" className='query1SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
