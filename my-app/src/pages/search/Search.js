import './Search.css';
import React, { useState, useEffect } from "react";
import axios from 'axios';
import UserNavbar from '../../components/navbar/UserNavbar';

export default function Search() {

    const userEmail = 'user@example.com';

    const handleLogout = () => {
        console.log('User logged out');
    };

    const [results, setResults] = useState([]);
    const [error, setError] = useState(null);

    const [area, setArea] = useState({ area: "" });
        
    const [options, setOptions] = useState({
        area_names: [],
    });

    useEffect(() => {
        // Fetch dropdown options from Django backend
        axios.get("http://127.0.0.1:8000/api/db_manager/dropdown-options/")
        .then((response) => {
            setOptions(response.data);
        })
        .catch((error) => {
            console.error("Error fetching dropdown options:", error);
        });
    }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setArea((prevTimes) => ({
      ...prevTimes,
      [name]: value,
    }));
    };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); 

    try {
      const response = await axios.get('http://127.0.0.1:8000/api/db_manager/search/', {
        params: {
          area_name: area.area,
        },
      });

      if (response.data.message) {
        setError(response.data.message); 
      } else {
        setResults(response.data); 
      }
      
    } catch (err) {
      setError(err.response?.data?.error || "An unexpected error occurred.");
    }
  };

  const handleReset = () => {

    setArea({
      area: "",
    });
  
    setResults([]);
    setError(null);
  };

    return (
        <div className='search'>
            <UserNavbar userEmail={userEmail} onLogout={handleLogout} />
            <div className="search-bar">
            <form className="searchForm" onSubmit={handleSubmit}>
           
                   <label htmlFor="searchAreaName">Area</label>
                    <select
                    className="searchAreaName"
                    id="searchAreaName"
                    name="area_name"
                    placeholder="Select Area"
                    value={area.area}
                    onChange={handleChange}>
                    
                    <option value="" disabled>Select Area</option>
                    {options.area_names?.map((code, index) => (
                      <option key={index} value={code}>{code}</option>
                    ))}
                </select>
                {!results.length > 0 && (
                  <div className='searchSubmit'>
                    <button type="submit" className='searchSubmitButton'>Submit</button>
                  </div>
                )}
                </form>
                </div>
            {error && <div className='searchError'>{error}</div>}
            {results.length > 0 && (
              <div className="searchResults">
                <h4 className="searchResultsTitle">Results:</h4>
                <div className="resultsTableWrapper">
                  <table className="resultsTable">
                    <thead>
                      <tr>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Gap</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.map((result, index) => (
                        <tr key={index}>
                          <td>{result["start_date"]}</td>
                          <td>{result["end_date"]}</td>
                          <td>{result["gap"]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {results.length > 0 && (
              <button onClick={handleReset} className="searchSubmitButton">Reset</button>
            )}     
      </div>
  );
}

