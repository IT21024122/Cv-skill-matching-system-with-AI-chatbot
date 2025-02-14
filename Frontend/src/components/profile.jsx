// import React, { useState } from "react";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const ProfilePage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [validationResult, setValidationResult] = useState(null);
  const [statusValidationResult, setStatusValidationResult] = useState(null);
  
  const [recommendedJobTitle, setRecommendedJobTitle] = useState("title here");

  useEffect(() => {
    // Fetch initial job title recommendation
    const fetchInitialJobTitle = async () => {
      try {
        const response = await fetch("http://localhost:8000/predict_job/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            skills: ["python", "data analysis", "machine learning"],
          }),
        });
        const data = await response.json();
        setRecommendedJobTitle(data.recommended_job_title);
      } catch (error) {
        console.error("Error fetching initial job title:", error);
      }
    };

    fetchInitialJobTitle();
  }, []);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("pdf_file", selectedFile);
      formData.append(
        "validation_input",
        JSON.stringify({
          names: ["John Doe"],
          roles: ["Manager"],
          nic_numbers: ["199811820086V"],
          date_ranges: ["01 01 2020 to 31 12 2020"],
        })
      );
      //   formData.append("validation_input", validationInput);
      try {
        const response = await fetch("http://localhost:8000/extract-data/", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        setValidationResult(data.validation);
        setStatusValidationResult(data.status);
        // setValidationResult(response.data.validation);
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };
  return (
    <div>
      <nav class="bg-gray-800">
        <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
          <div class="relative flex h-16 items-center justify-between">
            <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
              <Link to="/">
                <div class="flex flex-shrink-0 items-center">
                  <img
                    class="h-8 w-auto"
                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                    alt="Your Company"
                  />
                </div>
                <div class="hidden sm:ml-6 sm:block"></div>
              </Link>
            </div>

            <div class="py-6">
              <a
                href="/login"
                class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-white hover:bg-gray-50 hover:text-black"
              >
                Log Out
              </a>
            </div>
          </div>
        </div>
      </nav>
      <div class="bg-white overflow-hidden shadow rounded-lg border">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            User Profile
          </h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            This is some information about the user.
          </p>
        </div>
        <div className="m-10">
          <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Full name</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  Gayan Kasun
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Email address</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  Gayan@gmail.com
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Phone number</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  0767-7159801
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Job Role</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  Ml Engineer
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Ofz</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  cxy ofz
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Date ranges</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  01 01 2020 to 31 12 2020
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Nic number</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  199811820086V
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Skills</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  python, data analysis, machine learning
                </dd>
              </div>
              <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">
                  Recommended Job Title
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  {recommendedJobTitle}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
      <div className="m-10">
        <input type="file" onChange={handleFileChange} />
        <button
          onClick={handleUpload}
          className="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Validate PDF
        </button>
        {statusValidationResult && (
        <h3 className="text-lg leading-6 font-medium text-gray-900">
            {statusValidationResult}
        </h3>
        )}
      </div>
      {validationResult && (
        <div className="mt-10">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Validation Results
          </h3>
          <table className="min-w-full mt-5">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Field
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(validationResult).map((key) => (
                <tr key={key}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {key}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {validationResult[key]}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
