import React from 'react';

const Hea = () => {
    return (
        <header className="blog-header lh-1 py-3">
        <div className="row flex-nowrap justify-content-between align-items-center">
          <div className="col-4 pt-1">
          </div>
          <div className="col-4 text-center">
            <a className="blog-header-logo text-dark" href="/">Definitely not a blog</a>
          </div>
          <div className="col-4 d-flex justify-content-end align-items-center">
            <a className="link-secondary" href="/" aria-label="Search">
            </a>
            <a className="btn btn-sm btn-outline-secondary" href="/">Sign up</a>
          </div>
        </div>
      </header>

    );
};

export default Hea;