import React from 'react';
import './App.css';
import Hea from './components/header';
import HeaderNav from "./components/header_nav";
import Posts from "./elements/Posts";
import Post from "./elements/Post"
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Comments from "./elements/Comments";
import Tag from "./elements/Tag";

function App() {
    return (
        <div className="App">
            <Hea/>
            <HeaderNav/>
            <article className="blog-post">
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<Posts/>}/>
                        <Route path="post">
                            <Route path=":id" element={<><Post/><Comments/></>}></Route>
                        </Route>
                        <Route path="/:tag" element={<Tag/>}/>
                    </Routes>
                </BrowserRouter>
            </article>
        </div>
    );
}

export default App;
