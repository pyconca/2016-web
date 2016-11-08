import React from 'react';
import utf8  from 'utf8';

let reEmptyBio = /<h2[^>]*>.+<\/h2>\s*$/m;


export default class Info extends React.Component {
    render() {
        let session = this.props.session;
        let room    = this.props.room;
        let html    = session.html;

        if (html && html.match(reEmptyBio)) {
            html = html.replace(reEmptyBio, '');
        }

        let summary = { __html: html };

        let roomLabel = room ? room.name : null;
        
        if (roomLabel === null) {
            roomLabel = 'General Area / Salle de Conférence';
            try {
                roomLabel = utf8.decode(roomLabel);
            } catch (e) {
                // Bypass due to Unicode handling issue in JavaScript.
            }
        }

        return (
            <div className="info">
                <a className="close" onClick={ this.props.onClick }></a>
                <h1>{ session.title }</h1>
                <div
                    className               = "speakers"
                    dangerouslySetInnerHTML = { { __html: session.speakers } }
                />
                <div className="metadata">
                    <div className="room">{ roomLabel }</div>
                    <div className="timestamp">
                        <span className="date">{ session.mStartTime.format('YYYY-MM-DD') }</span>
                        <span className="start">{ session.mStartTime.format('HH:mm') }</span>
                        <span className="end">{ session.mEndTime.format('HH:mm') }</span>
                    </div>
                    <span className="duration">{ session.durationInMinute }</span>
                </div>
                <div
                    className               = "summary"
                    dangerouslySetInnerHTML = { summary }
                />
            </div>
        );
    }
}
