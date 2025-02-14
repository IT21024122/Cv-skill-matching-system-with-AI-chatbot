import React, { useState, useRef } from "react";
import { FiPaperclip } from "react-icons/fi";
import { Link } from "react-router-dom";

import "../css/bootstrap.min.css";
import "../css/tooplate-gotto-job.css";

const PageTwo = () => {
  const [isChatboxOpen, setChatboxOpen] = useState(false);
  const [userInput, setUserInput] = useState("");
  const chatboxRef = useRef(null);
  const fileInputRef = useRef(null);

  const toggleChatbox = () => {
    setChatboxOpen((prev) => !prev);
  };

  const handleSendMessage = () => {
    if (userInput.trim() !== "") {
      addUserMessage(userInput);
      respondToUser(userInput);
      setUserInput("");
    }
  };

  const handleKeyUp = (event) => {
    if (event.key === "Enter") {
      handleSendMessage();
    }
  };

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log("File selected:", file);
      // Add logic to upload the file or handle it
    }
  };

  const handleFileClick = () => {
    fileInputRef.current.click();
  };

  const addUserMessage = (message) => {
    const chatbox = chatboxRef.current;
    const messageElement = document.createElement("div");
    messageElement.className = "mb-2 text-right";
    messageElement.innerHTML = `<p class="bg-blue-500 text-white rounded-lg py-2 px-4 inline-block">${message}</p>`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
  };

  const addBotMessage = (message) => {
    const chatbox = chatboxRef.current;
    const messageElement = document.createElement("div");
    messageElement.className = "mb-2";
    messageElement.innerHTML = `<p class="bg-gray-200 text-gray-700 rounded-lg py-2 px-4 inline-block">${message}</p>`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
  };

  const respondToUser = async (userMessage) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/process-message/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: userMessage,
          user: "test_user",
        }),
      });

      const data = await response.json();

      data.bot_responses.forEach((botMessage) => addBotMessage(botMessage));
    } catch (error) {
      console.error("Error responding to user:", error);
      addBotMessage("Sorry, there was an error processing your request.");
    }
  };

  const [jobs] = useState([
    {
      id: 1,
      title: "Software Engineer",
      company: "TechCorp",
      location: "New York",
    },
    {
      id: 2,
      title: "Data Scientist",
      company: "DataWorks",
      location: "San Francisco",
    },
    {
      id: 3,
      title: "Product Manager",
      company: "Innovate LLC",
      location: "Boston",
    },
    {
      id: 4,
      title: "UI/UX Designer",
      company: "DesignHub",
      location: "Los Angeles",
    },
    {
      id: 5,
      title: "Software Engineer",
      company: "CodeBase",
      location: "Chicago",
    },
    {
      id: 6,
      title: "DevOps Engineer",
      company: "CloudNet",
      location: "Austin",
    },
    {
      id: 7,
      title: "Data Analyst",
      company: "InsightCorp",
      location: "Seattle",
    },
    { id: 8, title: "Project Manager", company: "BuildIt", location: "Denver" },
    {
      id: 9,
      title: "Frontend Developer",
      company: "WebMinds",
      location: "Miami",
    },
    {
      id: 10,
      title: "Software Engineer",
      company: "SoftSolutions",
      location: "Dallas",
    },
    {
      id: 11,
      title: "Backend Developer",
      company: "APIServices",
      location: "Atlanta",
    },
    {
      id: 12,
      title: "Data Scientist",
      company: "DataGurus",
      location: "New York",
    },
    {
      id: 13,
      title: "Cybersecurity Analyst",
      company: "SecureSys",
      location: "Phoenix",
    },
    {
      id: 14,
      title: "Machine Learning Engineer",
      company: "AIPros",
      location: "San Francisco",
    },
    {
      id: 15,
      title: "QA Engineer",
      company: "TestMasters",
      location: "Boston",
    },
    {
      id: 16,
      title: "Product Manager",
      company: "Visionary",
      location: "Los Angeles",
    },
    {
      id: 17,
      title: "System Administrator",
      company: "NetGuard",
      location: "Houston",
    },
    {
      id: 18,
      title: "Data Engineer",
      company: "DataFlow",
      location: "Chicago",
    },
    {
      id: 19,
      title: "Software Engineer",
      company: "TechBridge",
      location: "San Diego",
    },
    {
      id: 20,
      title: "UI/UX Designer",
      company: "CreativeMinds",
      location: "Portland",
    },
  ]);

  const [searchTerm, setSearchTerm] = useState("");

  const title1 = "Software Engineer"; // First title to filter
  const title2 = "Data Scientist"; // Second title to filter

  const filteredJobs = jobs.filter((job) => {
    const jobTitleLower = job.title.toLowerCase();
    return (
      (jobTitleLower.includes(title1.toLowerCase()) ||
        jobTitleLower.includes(title2.toLowerCase())) &&
      (job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.location.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  });

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
            <div>
              <Link to="/profile">
                <button
                  type="button"
                  class="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                  id="user-menu-button"
                  aria-expanded="false"
                  aria-haspopup="true"
                >
                  <span class="absolute -inset-1.5"></span>
                  <img
                    class="h-8 w-8 rounded-full"
                    src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    alt=""
                  />
                </button>
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

        <div class="sm:hidden" id="mobile-menu">
          <div class="space-y-1 px-2 pb-3 pt-2">
            <a
              href="#"
              class="block rounded-md bg-gray-900 px-3 py-2 text-base font-medium text-white"
              aria-current="page"
            >
              Dashboard
            </a>
            <a
              href="#"
              class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
            >
              Team
            </a>
            <a
              href="#"
              class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
            >
              Projects
            </a>
            <a
              href="#"
              class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
            >
              Calendar
            </a>
          </div>
        </div>
      </nav>
      <input
        type="text"
        placeholder="Search jobs by title, company, or location..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <section class="section-padding pb-0 d-flex justify-content-center align-items-center">
        <div class="container">
          <div class="row">
            <div class="col-lg-12 col-12">
              <form
                class="custom-form hero-form"
                action="#"
                method="get"
                role="form"
              >
                <h3 class="text-white mb-3">Search your dream job</h3>

                <div class="row">
                  <div class="col-lg-6 col-md-6 col-12">
                    <div class="input-group">
                      <span class="input-group-text" id="basic-addon1">
                        <i class="bi-person custom-icon"></i>
                      </span>

                      <input
                        type="text"
                        name="job-title"
                        id="job-title"
                        class="form-control"
                        placeholder="Job Title"
                        required
                      />
                    </div>
                  </div>

                  <div class="col-lg-6 col-md-6 col-12">
                    <div class="input-group">
                      <span class="input-group-text" id="basic-addon1">
                        <i class="bi-geo-alt custom-icon"></i>
                      </span>

                      <input
                        type="text"
                        name="job-location"
                        id="job-location"
                        class="form-control"
                        placeholder="Location"
                        required
                      />
                    </div>
                  </div>

                  <div class="col-lg-4 col-md-4 col-12">
                    <div class="input-group">
                      <span class="input-group-text" id="basic-addon1">
                        <i class="bi-cash custom-icon"></i>
                      </span>

                      <select
                        class="form-select form-control"
                        name="job-salary"
                        id="job-salary"
                        aria-label="Default select example"
                      >
                        <option selected>Salary Range</option>
                        <option value="1">$300k - $500k</option>
                        <option value="2">$10000k - $45000k</option>
                      </select>
                    </div>
                  </div>

                  <div class="col-lg-4 col-md-4 col-12">
                    <div class="input-group">
                      <span class="input-group-text" id="basic-addon1">
                        <i class="bi-laptop custom-icon"></i>
                      </span>

                      <select
                        class="form-select form-control"
                        name="job-level"
                        id="job-level"
                        aria-label="Default select example"
                      >
                        <option selected>Level</option>
                        <option value="1">Internship</option>
                        <option value="2">Junior</option>
                        <option value="2">Senior</option>
                      </select>
                    </div>
                  </div>

                  <div class="col-lg-4 col-md-4 col-12">
                    <div class="input-group">
                      <span class="input-group-text" id="basic-addon1">
                        <i class="bi-laptop custom-icon"></i>
                      </span>

                      <select
                        class="form-select form-control"
                        name="job-remote"
                        id="job-remote"
                        aria-label="Default select example"
                      >
                        <option selected>Remote</option>
                        <option value="1">Full Time</option>
                        <option value="2">Contract</option>
                        <option value="2">Part Time</option>
                      </select>
                    </div>
                  </div>

                  <div class="col-lg-12 col-12">
                    <button type="submit" class="form-control">
                      Search job
                    </button>
                  </div>

                  <div class="col-12">
                    <div class="d-flex flex-wrap align-items-center mt-4 mt-lg-0">
                      <span class="text-white mb-lg-0 mb-md-0 me-2">
                        Popular keywords:
                      </span>

                      <div>
                        <a href="job-listings.html" class="badge">
                          Web design
                        </a>

                        <a href="job-listings.html" class="badge">
                          Marketing
                        </a>

                        <a href="job-listings.html" class="badge">
                          Customer support
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <div class="col-lg-6 col-12">
              <img
                src="images/4557388.png"
                class="hero-image img-fluid"
                alt=""
              />
            </div>
          </div>
        </div>
      </section>
      <section class="job-section section-padding">
        <div class="container">
          <div class="row align-items-center">
            <div class="col-lg-6 col-12 mb-lg-4">
              <h3>Results of 30-65 of 1500 jobs</h3>
            </div>

            <div class="col-lg-4 col-12 d-flex align-items-center ms-auto mb-5 mb-lg-4">
              <p class="mb-0 ms-lg-auto">Sort by:</p>

              <div class="dropdown dropdown-sorting ms-3 me-4">
                <button
                  class="btn btn-secondary dropdown-toggle"
                  type="button"
                  id="dropdownSortingButton"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Newest Jobs
                </button>

                <ul
                  class="dropdown-menu"
                  aria-labelledby="dropdownSortingButton"
                >
                  <li>
                    <a class="dropdown-item" href="#">
                      Lastest Jobs
                    </a>
                  </li>

                  <li>
                    <a class="dropdown-item" href="#">
                      Highed Salary Jobs
                    </a>
                  </li>

                  <li>
                    <a class="dropdown-item" href="#">
                      Internship Jobs
                    </a>
                  </li>
                </ul>
              </div>

              <div class="d-flex">
                <a href="#" class="sorting-icon active bi-list me-2"></a>

                <a href="#" class="sorting-icon bi-grid"></a>
              </div>
            </div>

            {filteredJobs.length > 0 ? (
              filteredJobs.map((job) => (
                <div key={job.id} class="col-lg-4 col-md-6 col-12">
                  <div class="job-thumb job-thumb-box">
                    <div class="job-image-box-wrap">
                      <a href="job-details.html">
                        <img
                          src="images/jobs/it-professional-works-startup-project.jpg"
                          class="job-image img-fluid"
                          alt=""
                        />
                      </a>
                    </div>

                    <div class="job-body">
                      <h4 class="job-title">
                        <a href="job-details.html" class="job-title-link">
                          {job.title}
                        </a>
                      </h4>

                      <div class="d-flex align-items-center">
                        <div class="job-image-wrap d-flex align-items-center bg-white shadow-lg mt-2 mb-4">
                          <img
                            src="images/logos/salesforce.png"
                            class="job-image me-3 img-fluid"
                            alt=""
                          />

                          <p class="mb-0">{job.company}</p>
                        </div>

                        <a href="#" class="bi-bookmark ms-auto me-2"></a>

                        <a href="#" class="bi-heart"></a>
                      </div>

                      <div class="d-flex align-items-center">
                        <p class="job-location">
                          <i class="custom-icon bi-geo-alt me-1"></i>
                          {job.location}
                        </p>

                        <p class="job-date">
                          <i class="custom-icon bi-clock me-1"></i>
                          10 hours ago
                        </p>
                      </div>

                      <div class="d-flex align-items-center border-top pt-3">
                        <p class="job-price mb-0">
                          <i class="custom-icon bi-cash me-1"></i>
                          $50k
                        </p>

                        <a
                          href="job-details.html"
                          class="custom-btn btn ms-auto"
                        >
                          Apply now
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p>No jobs found.</p>
            )}

            <div class="col-lg-12 col-12">
              <nav aria-label="Page navigation example">
                <ul class="pagination justify-content-center mt-5">
                  <li class="page-item">
                    <a class="page-link" href="#" aria-label="Previous">
                      <span aria-hidden="true">Prev</span>
                    </a>
                  </li>

                  <li class="page-item active" aria-current="page">
                    <a class="page-link" href="#">
                      1
                    </a>
                  </li>

                  <li class="page-item">
                    <a class="page-link" href="#">
                      2
                    </a>
                  </li>

                  <li class="page-item">
                    <a class="page-link" href="#">
                      3
                    </a>
                  </li>

                  <li class="page-item">
                    <a class="page-link" href="#">
                      4
                    </a>
                  </li>

                  <li class="page-item">
                    <a class="page-link" href="#">
                      5
                    </a>
                  </li>

                  <li class="page-item">
                    <a class="page-link" href="#" aria-label="Next">
                      <span aria-hidden="true">Next</span>
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </section>
      <div
        className={`fixed bottom-0 right-0 mb-4 mr-4 ${
          isChatboxOpen ? "hidden" : ""
        }`}
      >
        <button
          onClick={toggleChatbox}
          className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300 flex items-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-6 h-6 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            ></path>
          </svg>
          Chat
        </button>
      </div>

      {isChatboxOpen && (
        <div id="chat-container" className="fixed bottom-16 right-4 w-96">
          <div className="bg-white shadow-md rounded-lg max-w-lg w-full">
            <div className="p-4 border-b bg-blue-500 text-white rounded-t-lg flex justify-between items-center">
              <p className="text-lg font-semibold">Chat</p>
              <button
                onClick={toggleChatbox}
                className="text-gray-300 hover:text-gray-400 focus:outline-none focus:text-gray-400"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-6 h-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  ></path>
                </svg>
              </button>
            </div>
            <div ref={chatboxRef} className="p-4 h-80 overflow-y-auto"></div>
            <div className="p-4 border-t flex items-center">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
              />
              <button
                onClick={handleFileClick}
                className="p-2 rounded-md border border-gray-200 hover:bg-gray-300 transition duration-300 mr-2"
              >
                <FiPaperclip className="w-6 h-6 text-gray-500" />
              </button>
              <input
                type="text"
                value={userInput}
                onChange={handleInputChange}
                onKeyUp={handleKeyUp}
                placeholder="Type a message"
                className="w-full px-3 py-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleSendMessage}
                className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition duration-300"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PageTwo;
