import React from 'react';
import c from 'classnames/bind';


class BaseLayout extends React.Component {
  render() {
    let { className, children } = this.props;
    return (
        <main className={ c( "main", className ) }>
          { children }
        </main>
    );
  }
}

class ContainerLayout extends React.Component {
  render() {
    let { className, children } = this.props;
    return (
        <BaseLayout className={ c( "container mt-5", className ) }>
          { children }
        </BaseLayout>
    );
  }
}

class CenterLayout extends React.Component {
  render() {
    let { className, children } = this.props;
    return (
        <BaseLayout className={ c( "d-flex flex-column justify-content-center align-items-center", className ) }>
          { children }
        </BaseLayout>
    );
  }
}

export { BaseLayout as default, ContainerLayout, CenterLayout };

