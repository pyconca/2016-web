import React from 'react';

import DaySchedule from './day_schedule.jsx';

export default class Core extends React.Component {
    render() {
        let timeline = this.props.timeline;
        let blocks   = [];

        for (let date of timeline.dates) {
            blocks.push(
                <h3 key = { date + '.label' }>{ date }</h3>
            );

            blocks.push(
                <DaySchedule
                    key      = { date }
                    schedule = { timeline.schedule[date] }
                    rooms    = { this.props.rooms }
                />
            );
        }

        return (
            <div className="core">{ blocks }</div>
        );
    }
}
