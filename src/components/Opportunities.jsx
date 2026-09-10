import Navbar from "./Navbar";
import OpportunitiesCard from "./OpportunitiesCard";
import "./OpportunitiesCard.css";

const opportunitiesData = [
    {
        id: 1,
        company: "Toyota",
        title: "Toyota Bursaries 2027",
        location: "South Africa",
        closingDate: "01/06/2026",
        applyUrl: "https://studytrust.org.za/toyota/",
    },
    {
        id: 2,
        company: "Discovery",
        title: "Cloud Architect",
        location: "South Africa",
        closingDate: "01/09/2026",
        applyUrl: "https://careers.discovery.co.za/job/Sandton-1-Discovery-Place-Cloud-Architect-GP-2196/1431943333/",
    },
];

function Opportunities () {

    return(
        <div className="opportunitiesPage">
            <Navbar/>
            <h1>Jobs & Opportunities Hub</h1>
            {opportunitiesData.map((opp) => (
                <OpportunitiesCard
                key={opp.id}
                company={opp.company}
                title={opp.title}
                location={opp.location}
                closingDate={opp.closingDate}
                applyUrl={opp.applyUrl}
                />
            )
            )}
        </div>
    );
}

export default Opportunities;