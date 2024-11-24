import './Insert.css';
import React, { useState, useEffect } from "react";
import axios from "axios";
import UserNavbar from '../../components/navbar/UserNavbar'; 

export default function Insert() {

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
        AreaDesc: "",
        PremisCd: "",
        PremisesDesc: "",
        CrmCd: "",
        Crime_codeDesc: "",
        CrmCd2: "",
        CrmCd3: "",
        CrmCd4: "",
        WeaponUsedCd: "",
        WeaponDesc: "",
        Location: "",
        Latitude: "",
        Longitude: "",
        CrossStreet: "",
        Status: "",
        StatusDesc: "",
    });

    const [options, setOptions] = useState({
        area_codes: [],
        crime_codes: [],
        premises: [],
        weapons: [],
        statuses: [],
    });

    const [editableFields, setEditableFields] = useState({
        AreaDesc: false,
        Crime_codeDesc: false,
        PremisesDesc: false,
        WeaponDesc: false,
        StatusDesc: false,
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

    const handleCodeChange = (e, type) => {
        const codeValue = e.target.value;

        setFormData((prevData) => ({
            ...prevData,
            [type]: codeValue,
            [`${type}Desc`]: "", // Reset description
        }));

        if (codeValue) {
            axios.get("http://127.0.0.1:8000/api/db_manager/get-code-description/", {
                params: { type, code: codeValue },
            })
            .then((response) => {
                setFormData((prevData) => ({
                    ...prevData,
                    [`${type}Desc`]: response.data.description,
                }));
                setEditableFields((prevFields) => ({
                    ...prevFields,
                    [`${type}Desc`]: false,
                }));
            })
            .catch((error) => {
                if (error.response && error.response.status === 404) {
                    setFormData((prevData) => ({
                        ...prevData,
                        [`${type}Desc`]: "",
                    }));
                    setEditableFields((prevFields) => ({
                        ...prevFields,
                        [`${type}Desc`]: true,
                    }));
                }
            });
        } else {
            setEditableFields((prevFields) => ({
                ...prevFields,
                [`${type}Desc`]: false,
            }));
        }
    };

    const generateDRNO = (areaCode, dateRptd) => {
        if (areaCode && dateRptd) {
            axios
                .get("http://127.0.0.1:8000/api/db_manager/generate-drno/", {
                    params: { area_id: areaCode, date_rptd: dateRptd },
                })
                .then((response) => {
                    setFormData((prevData) => ({
                        ...prevData,
                        DR_NO: response.data.DR_NO, 
                    }));
                })
                .catch((error) => {
                    console.error("Error generating DR_NO:", error);
                });
        } else {
            console.warn("AreaCode and DateRptd are required to generate DR_NO.");
            setFormData((prevData) => ({
                ...prevData,
                DR_NO: "",
            }));
        }
    };



    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
        ...prevData,
        [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const finalData = { ...formData };
        ["Area","CrmCd", "PremisCd", "WeaponUsedCd", "Status"].forEach((type) => {
        finalData[`${type}Desc`] = editableFields[`${type}Desc`]
            ? formData[`${type}DescCustom`]
            : formData[`${type}Desc`];
        });
        console.log(finalData);
    };


    return (
        <div className="insert">
            <UserNavbar userEmail={userEmail} onLogout={handleLogout} />
                <div className="insertFormContainer">
                <form className="insertForm" onSubmit={handleSubmit}>
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="DR_NO">DR_NO</label>
                        <input id="DR_NO" name="DR_NO" value={formData.DR_NO} readOnly type="text"/>
                    </div>
                    <div className="formField">
                        <label htmlFor="DateRptd">Date Rptd</label>
                        <input
                            id="DateRptd"
                            name="DateRptd"
                            value={formData.DateRptd}
                            onChange={(e) => {
                                const dateRptd = e.target.value;
                                handleChange(e);
                                if (formData.AreaCode) { generateDRNO(formData.AreaCode, dateRptd); } 
                            }}
                            type="date"
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
                        type="date"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="TimeOcc">TIME OCC</label>
                        <input
                        id="TimeOcc"
                        name="TimeOcc"
                        value={formData.TimeOcc}
                        onChange={handleChange}
                        type="time"
                        />
                    </div>
                    </div>

                    {/* Dropdown για Area Code */}
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="AreaCode">Area Code</label>
                        <select
                            id="AreaCode"
                            name="AreaCode"
                            value={formData.AreaCode}
                            onChange={(e) => {
                                const areaCode = e.target.value;
                                handleCodeChange(e, "Area");
                                if (formData.DateRptd) {generateDRNO(areaCode, formData.DateRptd);}
                            }}
                        >
                        <option value="">Select Area Code</option>
                        {options.area_codes.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.AreaCode === "custom" && (
                        <input
                            type="text"
                            name="CustomAreaCode"
                            placeholder="Enter new Area Code"
                            value={formData.AreaCode}
                            onChange={(e) => {
                                handleChange(e);
                                generateDRNO();
                            }}
                        />
                        )}
                    </div>
 
                    <div className="formField">
                        <label htmlFor="AreaName">Area Name</label>
                        {editableFields.AreaDesc? (
                        <input
                            type="text"
                            id="AreaNameCustom"
                            name="AreaNameCustom"
                            placeholder="Enter new Area Name"
                            value={formData.AreaDesc}
                            onChange={handleChange}
                        />
                        ) : (
                        <input
                            type="text"
                            id="AreaName"
                            name="AreaName"
                            value={formData.AreaDesc}
                            readOnly
                        />
                        )}
                    </div>
                    </div>
                            
                    {/* Dropdown -> Crime Code */}
                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="CrmCd">Crime Code</label>
                            <select
                                id="CrmCd"
                                name="CrmCd"
                                value={formData.CrmCd}
                                onChange={(e) => handleCodeChange(e, "Crime_code")}
                            >
                            <option value="">Select Crime Code</option>
                            {options.crime_codes.map((crime, index) => (
                                <option key={index} value={crime}>{crime}</option>
                            ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.CrmCd === "custom" && (
                        <input
                            type="text"
                            name="CustomCrimeCode"
                            placeholder="Enter new Crime Code"
                            value={formData.CrmCd}
                            onChange={handleChange}
                        />
                        )}
                    </div>
                    <div className="formField">
                        <label htmlFor="CrmCdDesc">Crime Description</label>
                        {editableFields.Crime_codeDesc ? (
                            <input
                                type="text"
                                id="CrmCdDescCustom"
                                name="CrmCdDescCustom"
                                placeholder="Enter new description"
                                value={formData.Crime_codeDesc}
                                onChange={handleChange}
                            />
                            ) : (
                            <input
                                type="text"
                                id="CrmCdDesc"
                                name="CrmCdDesc"
                                value={formData.Crime_codeDesc}
                                readOnly
                            />
                            )}
                    </div>
                    <div className="formField">
                        <label htmlFor="CrmCd2">Crm Cd 2</label>
                        <select
                            id="CrmCd2"
                            name="CrmCd2"
                            value={formData.CrmCd2}
                            onChange={handleChange}
                        >
                        <option value="">Select Crime Code</option>
                        {options.crime_codes.map((crime, index) => (
                            <option key={index} value={crime}>{crime}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.CrmCd2 === "custom" && (
                        <input
                            type="text"
                            name="CrmCd2Custom"
                            placeholder="Enter new Crime Code"
                            value={formData.CrmCd2}
                            onChange={handleChange}
                        />
                        )}
                    </div>
                    <div className="formField">
                        <label htmlFor="CrmCd3">Crm Cd 3</label>
                        <select
                        id="CrmCd3"
                        name="CrmCd3"
                        value={formData.CrmCd3}
                        onChange={handleChange}
                        >
                        <option value="">Select Crime Code</option>
                        {options.crime_codes.map((crime, index) => (
                            <option key={index} value={crime}>{crime}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.CrmCd3 === "custom" && (
                        <input
                            type="text"
                            name="CrmCdCustom3"
                            placeholder="Enter new Crime Code"
                            value={formData.CrmCd3}
                            onChange={handleChange}
                        />
                        )}
                    </div>
                    <div className="formField">
                        <label htmlFor="CrmCd4">Crm Cd 4</label>
                        <select
                        id="CrmCd4"
                        name="CrmCd4"
                        value={formData.CrmCd4}
                        onChange={handleChange}
                        >
                        <option value="">Select Crime Code</option>
                        {options.crime_codes.map((crime, index) => (
                            <option key={index} value={crime}>{crime}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.CrmCd4 === "custom" && (
                        <input
                            type="text"
                            name="CrmCdCustom4"
                            placeholder="Enter new Crime Code"
                            value={formData.CrmCd4}
                            onChange={handleChange}
                        />
                        )}
                    </div>
                    </div>
                    
                    <div className="formRow">
                     <div className="formField">
                        <label htmlFor="PremisCd">Premis Cd</label>
                        <select
                            id="PremisCd"
                            name="PremisCd"
                            value={formData.PremisCd}
                             onChange={(e) => handleCodeChange(e, "Premises")}
                        >
                        <option value="">Select Premis Cd</option>
                        {options.premises.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.PremisCd === "custom" && (
                        <input
                            type="text"
                            name="CustomPremisCd"
                            placeholder="Enter new Premis Cd"
                            value={formData.PremisCd}
                            onChange={handleChange}
                        />
                        )}
                    </div>
 
                    <div className="formField">
                        <label htmlFor="PremisDesc">Premis Desc</label>
                        {editableFields.PremisesDesc ? (
                        <input
                            type="text"
                            id="PremisDescCustom"
                            name="PremisDescCustom"
                            placeholder="Enter new Premis Desc"
                            value={formData.PremisesDesc}
                            onChange={handleChange}
                        />
                        ) : (
                        <input
                            type="text"
                            id="PremisDesc"
                            name="PremisDesc"
                            value={formData.PremisesDesc}
                            readOnly
                        />
                        )}
                    </div>
                    </div>

                    <div className="formRow">
                      <div className="formField">
                        <label htmlFor="WeaponUsedCd">Weapon Used Cd</label>
                        <select
                            id="WeaponUsedCd"
                            name="WeaponUsedCd"
                            value={formData.WeaponUsedCd}
                             onChange={(e) => handleCodeChange(e, "Weapon")}
                        >
                        <option value="">Select Weapon Used Cd</option>
                        {options.weapons.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.WeaponUsedCd === "custom" && (
                        <input
                            type="text"
                            name="CustomWeaponUsedCd"
                            placeholder="Enter new Weapon Used Cd"
                            value={formData.WeaponUsedCd}
                            onChange={handleChange}
                        />
                        )}
                    </div>
 
                    <div className="formField">
                        <label htmlFor="WeaponDesc">Weapon Desc</label>
                        {editableFields.WeaponDesc ? (
                        <input
                            type="text"
                            id="WeaponDescCustom"
                            name="WeaponDescCustom"
                            placeholder="Enter new Weapon Desc"
                            value={formData.WeaponDesc}
                            onChange={handleChange}
                        />
                        ) : (
                        <input
                            type="text"
                            id="WeaponDesc"
                            name="WeaponDesc"
                            value={formData.WeaponDesc}
                            readOnly
                        />
                        )}
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
                        type="number"
                        step="0.000001"
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="Longitude">Longitude</label>
                        <input
                        id="Longitude"
                        name="Longitude"
                        value={formData.Longitude}
                        onChange={handleChange}
                        type="number"
                        step="0.000001"
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
                        <select
                            id="Status"
                            name="Status"
                            value={formData.Status}
                             onChange={(e) => handleCodeChange(e, "Status")}
                        >
                        <option value="">Select Status</option>
                        {options.statuses.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.Status === "custom" && (
                        <input
                            type="text"
                            name="CustomStatus"
                            placeholder="Enter new Status"
                            value={formData.Status}
                            onChange={handleChange}
                        />
                        )}
                    </div>
 
                    {/* Αυτόματο ή custom Status Desc */}
                    <div className="formField">
                        <label htmlFor="StatusDesc">Status Desc</label>
                        {editableFields.StatusDesc ? (
                        <input
                            type="text"
                            id="StatusDescCustom"
                            name="StatusDescCustom"
                            placeholder="Enter new Status Desc"
                            value={formData.StatusDesc}
                            onChange={handleChange}
                        />
                        ) : (
                        <input
                            type="text"
                            id="StatusDesc"
                            name="StatusDesc"
                            value={formData.StatusDesc}
                            readOnly
                        />
                        )}
                    </div>
                    </div>
                    <button type="submit" className="submitButton">Submit</button>
                </form>
            </div>
        </div>
  );
}
