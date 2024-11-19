import './Query8.css';
import React, { useState } from "react";

export default function Query8() {
  const [isFormVisible, setIsFormVisible] = useState(false);

  const toggleFormVisibility = () => {
    setIsFormVisible((prev) => !prev);
  };

  const [dates, setDates] = useState({
    startDate: "",
    endDate: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDates((prevDates) => ({
      ...prevDates,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Start Date:", dates.startDate);
    console.log("End Date:", dates.endDate);
  };

  return (
    <div className='query8'>
      <div className='query8Box'>
        <div className='query8Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query8Desc'> Find the second most common crime that has co-occurred with a particular crime for a specific date range.</span>
        </div>
        <hr className='query8Line' />
        {isFormVisible && (
          <>
            <div className='query8Middle'>
              <form className='query8Form' onSubmit={handleSubmit}>
                <div className='startDate'>
                  <label htmlFor="startDate">Start Date</label>
                  <input className='startDateInput' type="date" id="startDate" name="startDate" value={dates.startDate} onChange={handleChange} />
                </div>
                <div className='endDate'>
                  <label htmlFor="endDate">End Date</label>
                  <input className='endDateInput' type="date" id="endDate" name="endDate" value={dates.endDate} onChange={handleChange} />
                </div>
              </form>
            </div>
            <div className='query8Down'>
              <button type="submit" className='query8SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
