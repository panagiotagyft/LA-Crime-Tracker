import './Updates.css';
import React, { useState } from "react";
import UserNavbar from '../../components/navbar/UserNavbar'; 

export default function Updates() {
  const userEmail = 'user@example.com';

  const handleLogout = () => {
    console.log('User logged out');
    };
    
  const [formData, setFormData] = useState({
    DR_NO: "",
    DateRptd: "",
    DateOcc: "",
    TimeOcc: "",
    AreaCode: "",
    AreaName: "",
    RptDistNo: "",
    CrmCd: "",
    CrmCdDesc: "",
    CrmCd2: "",
    CrmCd3: "",
    CrmCd4: "",
    ModusOperandi: "",
    VictimAge: "",
    VictimSex: "",
    VictimDescent: "",
    PremisCd: "",
    PremisDesc: "",
    WeaponUsedCd: "",
    WeaponDesc: "",
    Location: "",
    Latitude: "",
    Longitude: "",
    CrossStreet: "",
    Status: "",
    StatusDesc: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
    // Add API call or data handling logic here
  };

    return (
        <div className="updates">
            <UserNavbar userEmail={userEmail} onLogout={handleLogout} />
                <div className="updatesFormContainer">
                <form className="updatesForm" onSubmit={handleSubmit}>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="DR_NO">DR_NO</label>
                        <input
                        id="DR_NO"
                        name="DR_NO"
                        value={formData.DR_NO}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="DateRptd">Date Rptd</label>
                        <input
                        id="DateRptd"
                        name="DateRptd"
                        value={formData.DateRptd}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    </div>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="DateOcc">DATE OCC</label>
                        <input
                        id="DateOcc"
                        name="DateOcc"
                        value={formData.DateOcc}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="TimeOcc">TIME OCC</label>
                        <input
                        id="TimeOcc"
                        name="TimeOcc"
                        value={formData.TimeOcc}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    </div>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="PremisCd">Premis Cd</label>
                        <input
                        id="PremisCd"
                        name="PremisCd"
                        value={formData.PremisCd}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="PremisDesc">Premis Desc</label>
                        <input
                        id="PremisDesc"
                        name="PremisDesc"
                        value={formData.PremisDesc}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    </div>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="WeaponUsedCd">Weapon Used Cd</label>
                        <input
                        id="WeaponUsedCd"
                        name="WeaponUsedCd"
                        value={formData.WeaponUsedCd}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="WeaponDesc">Weapon Desc</label>
                        <input
                        id="WeaponDesc"
                        name="WeaponDesc"
                        value={formData.WeaponDesc}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    </div>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="Location">Location</label>
                        <input
                        id="Location"
                        name="Location"
                        value={formData.Location}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="Latitude">Latitude</label>
                        <input
                        id="Latitude"
                        name="Latitude"
                        value={formData.Latitude}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="Longitude">Longitude</label>
                        <input
                        id="Longitude"
                        name="Longitude"
                        value={formData.Longitude}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="CrossStreet">Cross Street</label>
                        <input
                        id="CrossStreet"
                        name="CrossStreet"
                        value={formData.CrossStreet}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    </div>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="Status">Status</label>
                        <input
                        id="Status"
                        name="Status"
                        value={formData.Status}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="StatusDesc">Status Desc</label>
                        <input
                        id="StatusDesc"
                        name="StatusDesc"
                        value={formData.StatusDesc}
                        onChange={handleChange}
                        type="text"
                        />
                    </div>
                    </div>
                    <button type="submit" className="submitButton">Submit</button>
                </form>
            </div>
        </div>
  );
}
