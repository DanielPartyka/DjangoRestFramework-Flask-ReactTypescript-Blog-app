import React, {useEffect, useState} from 'react';
import {PostsI} from "../interface/post";

const ShowPosts = () => {
        const [posts, setPosts] = useState([] as PostsI[]);

    useEffect(() => {
        (
            async () => {
                const response = await fetch('http://localhost:8000/api/posts')
                const data = await response.json()
                let i = 0;
                data.map(async (d: any) => {
                    const response_user = await fetch(`http://localhost:8000/api/users/${d.user_id}`)
                    const data_user = await response_user.json()
                    d.nick = data_user['nickname']
                })
                setPosts(data)

            }
        )();
    }, []);

    const dislike = async (id: number) => {
        await fetch(`http://localhost:8001/api/posts/${id}/dislike`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        setPosts(posts.map(
            (po: PostsI) => {
                if (po.id === id) {
                    po.dislikes++;
                }
                return po;
            }
        ))
    }
    const like = async (id: number) => {
        await fetch(`http://localhost:8001/api/posts/${id}/like`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        setPosts(posts.map(
            (po: PostsI) => {
                if (po.id === id) {
                    po.likes++;
                }
                return po;
            }
        ))
    }
    return (
        <div>
            {posts.map((p: PostsI) => {
                return (
                    <div>
                        <h3 className="pb-4 mb-4 fst-italic border-bottom">
                        </h3>
                        <a style={{textDecoration: 'none', color: "#000000"}} href="/"><h2
                            className="blog-post-title mb-1">{p.topic}</h2></a>
                        {
                            <p className="blog-post-meta">
                                {
                                    p.tags.map((tag) =>
                                        <a style={{textDecoration: 'none'}} href={"/" + tag}>#{tag}&nbsp;</a>
                                    )
                                }
                            </p>
                        }
                        <p className="blog-post-meta">Likes: {p.likes}, Dislikes: {p.dislikes}</p>
                        <p className="blog-post-meta">Added January 1, 2021 <a href="/">{p.user_id}</a></p>
                        <p>{p.text}</p>
                        <button type="button" className="btn btn-outline-success" onClick={() => like(p.id)}>Like
                        </button>
                        <button type="button" className="btn btn-outline-danger" onClick={() => dislike(p.id)}>Dislike
                        </button>

                    </div>
                )
            })}
        </div>
    );
};

export default ShowPosts;