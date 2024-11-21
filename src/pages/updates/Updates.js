// import './Updates.css';
// import React, { useState } from "react";

// export default function updates() {
//   const [isFormVisible, setIsFormVisible] = useState(false);

//   const toggleFormVisibility = () => {
//     setIsFormVisible((prev) => !prev);
//   };

//   const [times, setTimes] = useState({
//     startTime: "",
//     endTime: "",
//   });

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setTimes((prevTimes) => ({
//       ...prevTimes,
//       [name]: value,
//     }));
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     console.log("Start Time:", times.startTime);
//     console.log("End Time:", times.endTime);
//   };

//   return (
//     <div className='updates'>
//       <div className='updatesBox'>
//         <div className='updatesUp' onClick={toggleFormVisibility} style={{ cursor: 'pointer' }}>
//           <span className='updatesDesc'>1. Find the total number of reports per “Crm Cd” that occurred within a specified time range and sort them in a descending order.</span>
//         </div>
//         <hr className='updatesLine' />
//         {isFormVisible && (
//           <>
//             <div className='updatesMiddle'>
//               <form className='updatesForm' onSubmit={handleSubmit}>
//                 <div className='startTime'>
//                   <label htmlFor="startTime">Start Time</label>
//                   <input className='startTimeInput' type="time" id="startTime" name="startTime" value={times.startTime} onChange={handleChange} />
//                 </div>
//                 <div className='endTime'>
//                   <label htmlFor="endTime">End Time</label>
//                   <input className='endTimeInput' type="time" id="endTime" name="endTime" value={times.endTime} onChange={handleChange} />
//                 </div>
//               </form>
//             </div>
//             <div className='updatesDown'>
//               <button type="submit" className='updatesSubmitButton'>Submit</button>
//             </div>
//           </>
//         )}
//       </div>
//     </div>
//   );
// }
