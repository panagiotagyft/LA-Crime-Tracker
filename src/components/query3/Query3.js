import './Query3.css';
import React, { useState } from "react";

export default function Query3() {
  const [isFormVisible, setIsFormVisible] = useState(false);

  const toggleFormVisibility = () => {
    setIsFormVisible((prev) => !prev);
  };

  const [date, setDate] = useState("");

  const handleChange = (e) => {
    setDate(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Selected Date:", date);
  };

  return (
    <div className='query3'>
      <div className='query3Box'>
        <div className='query3Up' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
          <span className='query3Desc'>3. Find the most common crime committed regardless of code 1, 2, 3, and 4, per area for a specific day.</span>
        </div>
        <hr className='query3Line' />
        {isFormVisible && (
          <>
            <div className='query3Middle'>
              <form className='query3Form' onSubmit={handleSubmit}>
                <div className='selectDate'>
                  <label htmlFor="date">Date</label>
                  <input className='dateInput' type="date" id="date" name="date" value={date} onChange={handleChange} />
                </div>
              </form>
            </div>
            <div className='query3Down'>
              <button type="submit" className='query3SubmitButton'>Submit</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
