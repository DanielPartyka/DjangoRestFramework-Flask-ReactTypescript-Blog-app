import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";
import {PostsI} from "../interface/post";

const Tag = () => {
    const [posts, setPosts] = useState([] as PostsI[]);
    const [nickname, setNickname] = useState([]);
    const [numberofposts, setNumberOfPosts] = useState([])
    const {tag} = useParams()

    useEffect(() => {
        (
            async () => {
                const response = await fetch(`http://localhost:8000/api/posts/tags/?tag=${tag}`)
                const amount_of_post_per_tag = await fetch(`http://localhost:8000/api/posts/tags/number/?tag=${tag}`)
                const number_of_posts_per_tag = await amount_of_post_per_tag.json()
                setNumberOfPosts(number_of_posts_per_tag)
                const data = await response.json()
                data.map(async (d: any) => {
                    const response_user = await fetch(`http://localhost:8000/api/users/${d.user_id}`)
                    const data_user = await response_user.json()
                    setNickname(data_user['nickname'])
                })
                setPosts(data)
            console.log(data[0])
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

    function Show_tag() {
        return (
            <h3>Found posts with {tag}: {numberofposts}</h3>
        )
    }
    return (
        <div>
            <Show_tag/>
            {posts.map((p: PostsI) => {
                return (
                    <div>
                        <h3 className="pb-4 mb-4 fst-italic border-bottom">
                        </h3>
                        <a style={{textDecoration: 'none', color: "#000000"}} href={"/post/" + p.id}><h2
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
                        <p className="blog-post-meta">Added January 1, 2021 <a href="/">{nickname}</a></p>
                        <p>{p.text}</p>
                        <button type="button" className="btn btn-outline-success" onClick={() => like(p.id)}>Like +
                        </button>
                        <button type="button" className="btn btn-outline-danger" onClick={() => dislike(p.id)}>Dislike -
                        </button>

                    </div>
                )
            })}
        </div>
    );
};

export default Tag;