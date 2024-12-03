import './Query1.css';
import React, { useState } from "react";
import axios from 'axios';

export default function Query1() {
  const [isFormVisible, setIsFormVisible] = useState(false); // Αρχικά η φόρμα είναι κρυφή
  const [times, setTimes] = useState({
    startTime: "",
    endTime: "",
  });
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const toggleFormVisibility = () => {
    setIsFormVisible((prev) => !prev); // Εναλλαγή μεταξύ ορατότητας και μη
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTimes((prevTimes) => ({
      ...prevTimes,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Καθαρισμός προηγούμενων σφαλμάτων

    try {
      const response = await axios.get('http://127.0.0.1:8000/api/db_manager/query1/', {
        params: {
          startTime: times.startTime,
          endTime: times.endTime,
        },
      });

      if (response.data.message) {
        setError(response.data.message); // Εμφάνιση μηνύματος αν δεν υπάρχουν δεδομένα
      } else {
        setResults(response.data); // Εμφάνιση αποτελεσμάτων
      }
      
    } catch (err) {
      setError(err.response?.data?.error || "An unexpected error occurred.");
    }
  };

  const handleReset = () => {
    // Καθαρισμός των πεδίων της φόρμας
    setTimes({
      startTime: "",
      endTime: "",
    });
    // Καθαρισμός αποτελεσμάτων
    setResults([]);
    // Κρύψιμο φόρμας
    setIsFormVisible(false);
    // Καθαρισμός σφαλμάτων
    setError(null);
  };

  return (
    <div className='query1'>
      <div className='query1Box'>
        {/* Περιγραφή που επεκτείνεται/συρρικνώνεται */}
        <div
          className='query1Up'
          onClick={toggleFormVisibility}
          style={{ cursor: 'pointer' }}
        >
          <span className='query1Desc'>
            1. Find the total number of reports per “Crm Cd” that occurred within a specified time range and sort them in a descending order.
          </span>
        </div>
        <hr className='query1Line' />
        {/* Εμφάνιση Φόρμας ή Πίνακα */}
        {isFormVisible && (
          <>
            <form className='query1Form' onSubmit={handleSubmit}>

              <div className='query1Middle'>
                <div className='startTime'>
                  <label htmlFor="startTime">Start Time</label>
                  <input className='startTimeInput' type="time" id="startTime" name="startTime" value={times.startTime} onChange={handleChange} />
                </div>
                <div className='endTime'>
                  <label htmlFor="endTime">End Time</label>
                  <input className='endTimeInput' type="time" id="endTime" name="endTime" value={times.endTime} onChange={handleChange} />
                </div>
              </div>
  
              {!results.length > 0 &&(
                <div className='query1Down'>
                <button type="submit" className='query1SubmitButton'>Submit</button>
              </div>)}

            </form>
           
            {error && <div className='query1Error'>{error}</div>}
            {results.length > 0 && (
              <div className='query1Results'>
                <h4 className='query1ResultsTitle'>Results:</h4>
                <div className="resultsTableWrapper">
                  <table className="resultsTable">
                    <thead>
                      <tr>
                        <th>Crime Code</th>
                        <th>Report Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.map((result, index) => (
                        <tr key={index}>
                          <td>{result.crm_cd}</td>
                          <td>{result.report_count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
            {results.length > 0 && (
              <button onClick={handleReset} className="query1SubmitButton">Reset</button>
            )}
          </>
        )}
      </div>
    </div>
  );
}
