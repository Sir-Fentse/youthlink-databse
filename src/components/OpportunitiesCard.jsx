import "./OpportunitiesCard.css";
function OpportunitiesCard({company, title, location, closingDate, applyUrl}) {
    return (
        <div className="cardBox">
            <p><strong>Company:</strong>{company}</p>
            <p><strong>Title Description:</strong>{title}</p>
            <p><strong>Location:</strong>{location}</p>
            <p><strong>Closing:</strong>{closingDate}</p>
            <a href={applyUrl} target ="_blank" rel="noopener noreferrer">
                Apply Now!
            </a>
        </div>


    );
}
export default OpportunitiesCard;