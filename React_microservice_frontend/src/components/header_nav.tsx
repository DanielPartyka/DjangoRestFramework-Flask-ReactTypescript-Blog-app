import React, {useEffect, useState} from 'react';
import {TagsI} from "../interface/tag"

const HeaderNav = () => {
    const [tags, setTags] = useState([]);

    useEffect(() => {
        (
            async () => {
                const response_tag_nav = await fetch('http://localhost:8000/api/tags')
                const data_tag_nav = await response_tag_nav.json()
                setTags(data_tag_nav)
            }
        )();
    }, []);
    return (
        <div>
            <div className="nav-scroller py-1 mb-2">
                <nav className="nav d-flex justify-content-between">
            {tags.map((t : TagsI) => {
                return (
                    <a className="p-2 link-secondary" href={"/" + t.text}>#{t.text}</a>
                )
            })}
                </nav>
            </div>
        </div>
    );
};

export default HeaderNav;