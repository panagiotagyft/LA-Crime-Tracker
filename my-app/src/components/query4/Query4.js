import './Query4.css';
import React, { useState } from "react";

export default function Query4() {
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
    <div className='query4'>
      <div className='query4Box'>
        <div className='query4Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query4Desc'>4. Find the total number of reports per “Crm Cd” that occurred within a specified date range and sort them in a descending order.</span>
        </div>
        <hr className='query4Line' />
        {isFormVisible && (
          <>
            <div className='query4Middle'>
              <form className='query4Form' onSubmit={handleSubmit}>
                <div className='startDate'>
                  <label htmlFor="startDate">Start Date</label>
                  <input className='startDateInput' type="date" id="startDate" name="startDate" value={dates.startDate} onChange={handleChange} />
                </div>
                <div className='endDate'>
                  <label htmlFor="endDate">End Date</label>
                  <input className='endDateInput' type="date" id="endDate" name="endDate" value={dates.endDate} onChange={handleChange}/>
                </div>
              </form>
            </div>
            <div className='query4Down'>
              <button type="submit" className='query4SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
