import React from 'react';
import utf8  from 'utf8';

import visualConfig from './day_schedule_config.jsx';


export default class Session extends React.Component {
    constructor() {
        super();

        this.state = {
            hover: false,
        };
    }

    render() {
        let zeroTimestamp = this.props.zeroTimestamp;
        let timestamp     = this.props.timestamp;
        let session       = this.props.session;
        let rooms         = this.props.rooms;

        let room             = this._room(rooms, session.room);
        let trackIndex       = this._roomIndex(rooms, session.room);
        let durationInMinute = session.durationInMinute;
        let progressInMinute = (timestamp - zeroTimestamp) / 1000 / 60;
        let heightPerMinute  = visualConfig.heightPerMinute;
        let xPosOffset       = 0;

        if (this.state.hover && durationInMinute < 30) {
            heightPerMinute *= visualConfig.shortSessionHeightBooster;
            xPosOffset       = visualConfig.shortSessionYPosShifter;
        }

        let originXOffset    = (100 / rooms.length) * trackIndex;
        let blockTop         = (visualConfig.heightPerMinute * progressInMinute) + 1;
        let blockWidth       = ((100 / rooms.length) - visualConfig.rightMargin);
        let blockHeight      = (heightPerMinute * durationInMinute) - visualConfig.bottomMargin;
        let readableTime     = timestamp.format(visualConfig.timeFormat);
        let roomCode         = session.room || 'general';
        let roomName         = room ? room.name : '';

        if (trackIndex === null) {
            blockWidth = 100;
        }

        let forceStyle = {
            zIndex : this.state.hover ? 1 : 0,
            left   : originXOffset + '%',
            width  : blockWidth    + '%',
            height : blockHeight   + 'px',
            top    : (blockTop + xPosOffset) + 'px',
        };

        return (
            <a
                className   = { ['session', this.state.hover ? 'hover' : ''].join(' ') }
                href        = { session.alias }
                data-key    = { session.alias }
                data-time   = { readableTime }
                data-room   = { roomCode }
                style       = { forceStyle }
                onClick     = { this._onClick.bind(this) }
                onMouseOver = { this._onMouseOver.bind(this) }
                onMouseOut  = { this._onMouseOut.bind(this) }
            >
                <div className="inner">
                    <div className="room">{ roomName }</div>
                    <div className="title">{ session.title }</div>
                    <div
                        className               = "speakers"
                        dangerouslySetInnerHTML = { { __html: session.speakers } }
                    />
                    <div className="period">
                        <span className="start">{ session.mStartTime.format(visualConfig.timeFormat) }</span>
                        <span className="end">{ session.mEndTime.format(visualConfig.timeFormat) }</span>
                    </div>
                </div>
            </a>
        );
    }

    _onClick(e) {
        let room = this._room(this.props.rooms, this.props.session.room);

        e.preventDefault();

        if (room === null) {
            return;
        }

        console.log(room);

        this.props.onClick({
            session : this.props.session,
            room    : room,
        });
    }

    _onMouseOver() {
        this.setState({hover: true});
    }

    _onMouseOut() {
        this.setState({hover: false});
    }

    _roomIndex(rooms, roomCode) {
        let index = 0;

        for (let room of rooms) {
            if (room.slug === roomCode) {
                return index;
            }

            index++;
        }

        return null;
    }

    _room(rooms, roomCode) {
        for (let room of rooms) {
            if (room.slug === roomCode) {
                return room;
            }
        }

        return null;
    }
}
