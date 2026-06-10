<?php
namespace CD\Content;
class Toc {

	private $content;
	public $count;
	private $title;
	private $level;
	private $text;

	/**
	 * @param string $content A post includes the headers.
	 */
	public function __construct( $content = '' ) {
		global $post;
		if ( is_object( $post ) ) {
			if ( empty( $content ) ) {
				$content = $post->post_content;
			}
			// echo '<pre>' . print_r( esc_html( $content ), true ) . '<pre>'; die;
			preg_match_all( "/<h(2)[^>]+>(.*)<\/h(2)+>/i", $content, $match );
			if ( empty( $match[0] ) && empty( $match[1] ) && empty( $match[2] ) ) {
				preg_match_all( "#<[hH](2)>(.*?)</[hH](2)>#is", $content, $match );
			}
			$this->content = $content;
			$this->count   = count( $match[0] );
			$this->title   = $match[0];
			$this->level   = $match[1];
			$this->text    = $match[2];
		}
	}


	/**
	 * Creates an array of table of contents data structure.
	 *
	 * @return array
	 */
	public function getDataToc() {
		$toc = [];

		$count = $this->count;
		$level = $this->level;
		$text  = $this->text;
		for ( $i = 0, $j = 0; $i < $count; $i ++, $j ++ ) {
			// the first header
			if ( $i === 0 ) {
				$toc[ $i ]['list_open']  = true;
				$toc[ $i ]['item_open']  = true;
				$toc[ $i ]['text']       = $text[ $i ];
				$toc[ $i ]['href']       = $this->getHref( $i );
				$toc[ $i ]['item_close'] = true;
				$toc[ $i ]['list_close'] = false;
				$toc[ $i ]['level']      = $level[ $i ];

				continue;
			}

			// the last header
			if ( $i === $count - 1 ) {
				$toc[ $i ]['list_open'] = $level[ $i ] > $level[ $i - 1 ];;
				$toc[ $i ]['item_open']  = true;
				$toc[ $j ]['text']       = $text[ $i ];
				$toc[ $j ]['href']       = $this->getHref( $i );
				$toc[ $i ]['item_close'] = true;
				$toc[ $i ]['list_close'] = true;
				$toc[ $i ]['level']      = $level[ $i ];
				$j ++;
				break;
			}

			$toc[ $j ]['list_open']  = $level[ $i ] > $level[ $i - 1 ];
			$toc[ $j ]['item_open']  = true;
			$toc[ $j ]['text']       = $text[ $i ];
			$toc[ $j ]['href']       = $this->getHref( $i );
			$toc[ $j ]['item_close'] = $level[ $i ] >= $level[ $i + 1 ];
			$toc[ $j ]['list_close'] = $level[ $i ] > $level[ $i + 1 ];
			$toc[ $j ]['level']      = $level[ $i ];

		}

		return $toc;
	}

	/**
	 * Adds Href tag to H2
	 *
	 * @return string
	 */
	public function getPostMarkup() {

		$content = $this->content;
		$count   = $this->count;
		$title   = $this->title;
		$level   = $this->level;


		for ( $i = 0; $i < $count; $i ++ ) {
			$pattern     = '/<h' . $level[$i] . '([^>]*)>/';
			$replacement = '<h' . $level[$i] . '$1 id="toc_' . $i . '">';

			//Add Toc Id to Header
			$new_title = preg_replace( $pattern,
				$replacement,
				$title[ $i ]
			);

//			Replace entire heading
			$content = str_replace( $title[ $i ],
				$new_title,
				$content );
		}

		return $content;
	}


	/**
	 * Generates the table of contents markup.
	 *
	 * All captured headings are H2 (the constructor only matches H2), so the
	 * list is intentionally flat. Emits a semantic <nav> landmark with a valid
	 * <ol> — earlier versions emitted a stray closing </li> before the first
	 * <li> and used a non-semantic <div>, which produced invalid markup.
	 *
	 * @param bool $is_widget_area True when rendered in the sidebar widget area.
	 *                             Controls the eyebrow label and a modifier
	 *                             class, and suppresses the trailing first-H2
	 *                             that the in-body variant re-emits.
	 *
	 * @return string
	 */
	public function getToc( $is_widget_area = false ) {
		$count = (int) $this->count;
		if ( $count < 1 ) {
			// Nothing to list. In-body callers still expect the first H2 back.
			return $is_widget_area ? '' : ( isset( $this->title[0] ) ? $this->title[0] : '' );
		}

		$variant = $is_widget_area ? 'toc--sidebar' : 'toc--inline';
		$pill    = $is_widget_area ? 'In this article' : 'Contents';

		$toc  = '<nav class="toc ' . $variant . '" aria-label="Table of contents">';
		$toc .= '<div class="toc__pill">' . $pill . '</div>';
		$toc .= '<ol>';
		for ( $i = 0; $i < $count; $i ++ ) {
			$text = isset( $this->text[ $i ] ) ? trim( $this->text[ $i ] ) : '';
			if ( '' === $text ) {
				continue;
			}
			$toc .= '<li><a href="' . $this->getHref( $i ) . '" class="toc__li">' . $text . '</a></li>';
		}
		$toc .= '</ol>';
		$toc .= '</nav>';

		if ( ! $is_widget_area ) {
			$toc .= $this->title[0];
		}

		return $toc;
	}


	/**
	 * Get a modified post with a content marked up for  table of contents.
	 *
	 * @return string
	 */
	public function getPostTocInContent() {
		$toc                        = $this->getToc();
		$first_h2                   = $this->title[0];

		$content_with_toc           = str_replace( $first_h2,
			$toc,
			$this->content
		);
		$this->content              = $content_with_toc;
		$marked_up_content_with_toc = $this->getPostMarkup();

		return $marked_up_content_with_toc;
	}

	/**
	 * Added for the desktop version with no sidebar.
	 * @return string
	 */
	public function getPostTocInContentNoToC() {
		$marked_up_content_with_toc = $this->getPostMarkup();

		return $marked_up_content_with_toc;
	}


	/**
	 * @access protected
	 * @return string
	 */
	protected function getHref( $str ) {
		return "#" . 'toc_' . $str;
	}
}
