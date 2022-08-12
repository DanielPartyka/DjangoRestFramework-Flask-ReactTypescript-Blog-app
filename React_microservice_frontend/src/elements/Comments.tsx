import React, {useEffect, useState} from 'react';
import {CommentI} from "../interface/comment";
import {useParams} from "react-router-dom";
import {PostsI} from "../interface/post";

const Comments = () => {
    const [comments, setComments] = useState([] as CommentI[]);
    const [comments_num, setCommentsNumber] = useState([])
    const {id} = useParams();

    useEffect(() => {
        (
            async () => {
                const response = await fetch(`http://localhost:8000/api/posts/${id}/comments`)
                const data = await response.json()
                const get_amount_comments = await fetch(`http://localhost:8000/api/posts/${id}/comments_number`)
                const comments_number = await get_amount_comments.json()
                setCommentsNumber(comments_number)
                setComments(data)

            }
        )();
    }, []);

    const dislike_comm = async (id_comm: number) => {
        await fetch(`http://localhost:8001/api/comments/${id_comm}/dislike`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        setComments(comments.map(
            (co: CommentI) => {
                if (co.id === id_comm) {
                    co.dislikes++;
                }
                return co;
            }
        ))
    }
    const like_comm = async (id_comm: number) => {
        await fetch(`http://localhost:8001/api/comments/${id_comm}/like`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        setComments(comments.map(
            (co: CommentI) => {
                if (co.id === id_comm) {
                    co.likes++;
                }
                return co;
            }
        ))
    }

    function Separator() {
        return (
            <h3 className="pb-4 mb-4 fst-italic border-bottom"></h3>
        )
    }

    function CommentNumber() {
        return (
            <h4>Comments ({comments_num})</h4>
        )
    }

    return (
        <div>
            <Separator/>
            <CommentNumber/>
            <Separator/>
            {comments.map((c: CommentI) => {
                return (
                        <div>
                            <p className="blog-post-meta">December 23, 2013 by <a href="/">Jacob</a></p>
                            <p className="blog-post-meta">Likes: {c.likes}, Dislikes: {c.dislikes}</p>
                            <p>{c.text}</p>
                            <button type="button" className="btn btn-outline-success" onClick={() => like_comm(c.id)}>Like +
                            </button>
                            <button type="button" className="btn btn-outline-danger"
                                    onClick={() => dislike_comm(c.id)}>Dislike -
                            </button>
                            <Separator/>
                        </div>
                );
            })}
        </div>
    );
};

export default Comments;