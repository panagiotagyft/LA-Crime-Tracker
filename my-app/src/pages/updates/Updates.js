import './Updates.css';
import React, { useState, useEffect } from "react";
import axios from "axios";
import UserNavbar from '../../components/navbar/UserNavbar'; 

export default function Updates() {

    const userEmail = 'user@example.com';

    const handleLogout = () => {
        console.log('User logged out');
    };

    const [changesLog, setChangesLog] = useState({});
        
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
        RptDistNo: "",
        Mocodes: "",
        VictAge: "",
        VictSex: "",
        VictDescent: "",
    });

    const [options, setOptions] = useState({
        area_codes: [],
        crime_codes: [],
        premises: [],
        weapons: [],
        statuses: [],
        rpt_dists: [],
        victims_sex: [],
        victims_descent: [],
        mocodes: [],
        dr_numbers: [],
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


    const loadRecordData = (drNo) => {
        axios.get(`http://127.0.0.1:8000/api/db_manager/get-record/?dr_no=${drNo}`)
            .then((response) => {
                const data = response.data;
                setFormData((prevData) => ({
                    ...prevData,
                    ...data, // Update all fields with the data from the backend.
                }));
            })
            .catch((error) => {
                console.error("Error fetching record data:", error);
                alert("Failed to fetch record data.");
            });
    };

    const handleDrNoChange = (e) => {
        const drNo = e.target.value;
        setFormData((prevData) => ({
            ...prevData,
            DR_NO: drNo,
        }));
        if (drNo) {
            loadRecordData(drNo); // It loads the data for the selected DR_NO.
        }
    };


    const handleCodeChange = (e, type) => {
        const codeValue = e.target.value;

        const codeKeyMap = {
            "Area": "AreaCode",
            "Crime_code": "CrmCd",
            "Premises": "PremisCd",
            "Weapon": "WeaponUsedCd",
            "Status": "Status",
        };

        const descKeyMap = {
            "Area": "AreaDesc",
            "Crime_code": "Crime_codeDesc",
            "Premises": "PremisesDesc",
            "Weapon": "WeaponDesc",
            "Status": "StatusDesc",
        };

        const codeKey = codeKeyMap[type];
        const descKey = descKeyMap[type];

        setFormData((prevData) => ({
            ...prevData,
            [codeKey]: codeValue,
            [descKey]: "", // Reset description
        }));
        // Record changes.
        setChangesLog((prevLog) => ({
            ...prevLog,
            [codeKey]: codeValue,
        }));

        if (codeValue) {
            axios.get("http://127.0.0.1:8000/api/db_manager/get-code-description/", {
                params: { type, code: codeValue },
            })
            .then((response) => {
                setFormData((prevData) => ({
                    ...prevData,
                    [descKey]: response.data.description,
                }));
                // Record changes.
                setChangesLog((prevLog) => ({
                    ...prevLog,
                    [descKey]: response.data.description,
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
                        [descKey]: "",
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

    const handleChange = (e) => {
        const { name, value } = e.target;

        // Update the formData.
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));

        // Record changes.
        setChangesLog((prevLog) => ({
            ...prevLog,
            [name]: value,
        }));
    };


    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Changes to be updated:", changesLog); // Εδώ βλέπετε τις αλλαγές που θα σταλούν.
        axios.post("http://127.0.0.1:8000/api/db_manager/update-record/", changesLog)
            .then((response) => {
                alert("Update successful");
            })
            .catch((error) => {
                console.error("Error during update:", error);
            });
    };
    



    return (
        <div className="updates">
            <UserNavbar userEmail={userEmail} onLogout={handleLogout} />
                <div className="updatesFormContainer">
                <form className="updatesForm" onSubmit={handleSubmit}>
                    
                    <div className="formRow">
                    
                    {/* --- DR_NO --- */}
                    <div className="formField">
                        <label htmlFor="DR_NO">DR_NO</label>
                            <select
                                id="DR_NO"
                                name="DR_NO"
                                value={formData.DR_NO || ""}
                                onChange={(e) => { handleChange(e); handleDrNoChange(e); }}
                            >
                            <option value="">Select DR_NO</option>
                            {options.dr_numbers.map((dr, index) => (
                                <option key={index} value={dr}>
                                    {dr}
                                </option>
                            ))}
                            </select>
                    </div>
                    
                    {/* --- DateRptd --- */}
                    <div className="formField">
                        <label htmlFor="DateRptd">Date Rptd</label>
                        <input id="DateRptd" name="DateRptd" value={formData.DateRptd} onChange={handleChange} type="date"/>
                    </div>
                    </div>

                    {/* ===== 2nd ROW ==== */}
                    <div className="formRow">

                    {/* --- DateOcc --- */}
                    <div className="formField">
                        <label htmlFor="DateOcc">DATE OCC</label>
                        <input id="DateOcc" name="DateOcc" value={formData.DateOcc} onChange={handleChange} type="date"/>
                    </div>
                    
                    {/* --- TimeOcc --- */}
                    <div className="formField">
                        <label htmlFor="TimeOcc">TIME OCC</label>
                        <input id="TimeOcc" name="TimeOcc" value={formData.TimeOcc} onChange={handleChange} type="time"/>
                    </div>
                    </div>

                    {/* Dropdown for Area Code */}
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
                                const areaCode = e.target.value;
                                handleChange(e);
                                // if (formData.DateRptd) {generateDRNO(areaCode, formData.DateRptd);}
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

                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="RptDistNo">Rpt Dist No</label>
                        <select
                            id="RptDistNo"
                            name="RptDistNo"
                            value={formData.RptDistNo}
                            onChange={handleChange}
                        >
                        <option value="">Select Rpt Dist No</option>
                        {options.rpt_dists.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.RptDistNo === "custom" && (
                        <input
                            type="number"
                            name="CustomRptDistNo"
                            placeholder="Enter new RptDistNo"
                            value={formData.RptDistNo}
                            onChange={handleChange}
                        />
                        )}
                    </div>
                    <div className="formField">
                        <label htmlFor="Mocodes">Mocodes</label>
                        <select
                            id="Mocodes"
                            name="Mocodes"
                            value={formData.Mocodes}
                            onChange={handleChange}
                        >
                        <option value="">Select Mocodes</option>
                        {options.mocodes.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                        {formData.Mocodes === "custom" && (
                        <input
                            type="text"
                            name="MocodesCustom"
                            placeholder="Enter new Mocodes"
                            value={formData.Mocodes}
                            onChange={handleChange}
                        />
                        )}
                    </div>
                    </div>

                    <div className="formRow">
                    <div className="formField">
                        <label htmlFor="VictAge">Victim Age</label>                     
                        <input
                            type="number"
                            name="VictAge"
                            placeholder="Enter new Victim Age"
                            value={formData.VictAge}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="formField">
                        <label htmlFor="VictSex">Victim Sex</label>
                        <select
                            id="VictSex"
                            name="VictSex"
                            value={formData.VictSex}
                            onChange={handleChange}
                        >
                        <option value="">Select Victim Sex</option>
                        {options.victims_sex.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        </select>
                    </div>
                    <div className="formField">
                        <label htmlFor="VictDescent">Victim Descent</label>
                        <select
                            id="VictDescent"
                            name="VictDescent"
                            value={formData.VictDescent}
                            onChange={handleChange}
                        >
                        <option value="">Select Victim Descent</option>
                        {options.victims_descent.map((code, index) => (
                            <option key={index} value={code}>{code}</option>
                        ))}
                        <option value="custom">Other (Add New)</option>
                        </select>
                    </div>
                    </div>

                    <button type="submit" className="submitButton">Submit</button>
                </form>
            </div>
        </div>
  );
}
