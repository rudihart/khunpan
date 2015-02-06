__author__ = 'Rudolf Hart'

import Tk.Board


class TargetBoard(Tk.Board):
    VERSION = '1.0.0';
    SIZE_FACTOR = 5
    DIVISION_SIZE = 0.25

    def scale_board(self):
        zoom   = $SIZE_FACTOR * $self->cget('-zoom');
        board  = $self->cget('-board');
        self->scale( 'board', 0, 0, $zoom / 2, $zoom / 2 );
        self->move(
            'all',
            ( $board->{xmax} + 1 ) * $DIVISION_SIZE * $zoom,
            ( $board->{ymax} + 1 ) * $DIVISION_SIZE * $zoom

sub scale_piece {
    my ( $self, $piece ) = @_;
    my $zoom  = $self->cget('-zoom');
    my $board = $self->cget('-board');

    $self->scale( $piece->{name}, 0, 0, $zoom / 2, $zoom / 2 );
    $self->move(
        $piece->{name},
        ( $board->{xmax} + 1 ) * $DIVISION_SIZE * $zoom * $SIZE_FACTOR,
        ( $board->{ymax} + 1 ) * $DIVISION_SIZE * $zoom * $SIZE_FACTOR
    );
    return;
}

sub add_sensors {
    my ( $self, $piece ) = @_;

    # no sensors in target board
    return;
}

1;