import './Query7.css';
import React, { useState } from "react";

export default function Query7() {
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
    <div className='query7'>
      <div className='query7Box'>
        <div className='query7Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query7Desc'>Find the pair of crimes that has co-occurred in the area with the most reported incidents for a specific date range.</span>
        </div>
        <hr className='query7Line' />
        {isFormVisible && (
          <>
            <div className='query7Middle'>
              <form className='query7Form' onSubmit={handleSubmit}>
                <div className='startDate'>
                  <label htmlFor="startDate">Start Date</label>
                  <input
                    className='startDateInput'
                    type="date"
                    id="startDate"
                    name="startDate"
                    value={dates.startDate}
                    onChange={handleChange}
                  />
                </div>
                <div className='endDate'>
                  <label htmlFor="endDate">End Date</label>
                  <input
                    className='endDateInput'
                    type="date"
                    id="endDate"
                    name="endDate"
                    value={dates.endDate}
                    onChange={handleChange}
                  />
                </div>
              </form>
            </div>
            <div className='query7Down'>
              <button type="submit" className='query7SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
